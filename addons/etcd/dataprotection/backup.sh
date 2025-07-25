#!/var/run/etcd/bin/bash
export PATH=/var/run/etcd/bin:$PATH
set -exo pipefail

# if the script exits with a non-zero exit code, touch a file to indicate that the backup failed,
# the sync progress container will check this file and exit if it exists
handle_exit() {
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
    echo "failed with exit code $exit_code"
    touch "${DP_BACKUP_INFO_FILE}.exit"
    exit 1
  fi
}
trap handle_exit EXIT

# use etcdctl create snapshot
ENDPOINT="$DP_DB_HOST.$CLUSTER_NAMESPACE.svc$CLUSTER_DOMAIN:2379"
exec_etcdctl "${ENDPOINT}" snapshot save "${DP_BACKUP_NAME}"

# check the backup file, make sure it is not empty
check_backup_file "${DP_BACKUP_NAME}"

# use datasafed to get backup size
# if we do not write into $DP_BACKUP_INFO_FILE, the backup job will stuck
export PATH="$PATH:$DP_DATASAFED_BIN_PATH"
export DATASAFED_BACKEND_BASE_PATH="$DP_BACKUP_BASE_PATH"

tar -cvf - "${DP_BACKUP_NAME}" | datasafed push -z zstd-fastest - "${DP_BACKUP_NAME}.tar.zst"

TOTAL_SIZE=$(datasafed stat / | grep TotalSize | awk '{print $2}')
echo "{\"totalSize\":\"$TOTAL_SIZE\"}" >"${DP_BACKUP_INFO_FILE}" && sync
