{{/*
Data volume claim
*/}}
{{- define "milvus.vct.data" }}
- name: data
  spec:
    storageClassName: {{ .Values.persistence.data.storageClassName }}
    accessModes:
      - ReadWriteOnce
    resources:
      requests:
        storage: {{ print .Values.persistence.data.size "Gi" }}
{{- end }}

{{/*
External meta storage service reference
*/}}
{{- define "milvus.serviceRef.meta" }}
{{- if eq .Values.storage.meta.mode "serviceref" }}
- name: milvus-meta-storage
  namespace: {{ .Values.storage.meta.serviceRef.namespace }}
  {{- if .Values.storage.meta.serviceRef.cluster }}
  clusterServiceSelector:
    cluster: {{ .Values.storage.meta.serviceRef.cluster.name }}
    service:
      component: {{ .Values.storage.meta.serviceRef.cluster.component }}
      service: {{ .Values.storage.meta.serviceRef.cluster.service }}
      port: {{ .Values.storage.meta.serviceRef.cluster.port }}
     {{- if .Values.storage.meta.serviceRef.cluster.credential }}
    credential:
      component: {{ .Values.storage.meta.serviceRef.cluster.component }}
      name: {{ .Values.storage.meta.serviceRef.cluster.credential }}
    {{- end }}
  {{- end }}
  serviceDescriptor: {{ .Values.storage.meta.serviceRef.serviceDescriptor }}
{{- end }}
{{- end }}

{{/*
External log storage service reference
*/}}
{{- define "milvus.serviceRef.log" }}
{{- if eq .Values.storage.log.mode "serviceref" }}
- name: milvus-log-storage
  namespace: {{ .Values.storage.log.serviceRef.namespace }}
  {{- if .Values.storage.log.serviceRef.cluster }}
  clusterServiceSelector:
    cluster: {{ .Values.storage.log.serviceRef.cluster.name }}
    service:
      component: {{ .Values.storage.log.serviceRef.cluster.component }}
      service: {{ .Values.storage.log.serviceRef.cluster.service }}
      port: {{ .Values.storage.log.serviceRef.cluster.port }}
    {{- if .Values.storage.log.serviceRef.cluster.credential }}
    credential:
      component: {{ .Values.storage.log.serviceRef.cluster.component }}
      name: {{ .Values.storage.log.serviceRef.cluster.credential }}
    {{- end }}
  {{- end }}
  serviceDescriptor: {{ .Values.storage.log.serviceRef.serviceDescriptor }}
{{- end }}
{{- end }}

{{/*
External object storage service reference
*/}}
{{- define "milvus.serviceRef.object" }}
{{- if eq .Values.storage.object.mode "serviceref" }}
- name: milvus-object-storage
  namespace: {{ .Values.storage.object.serviceRef.namespace }}
  {{- if .Values.storage.object.serviceRef.cluster }}
  clusterServiceSelector:
    cluster: {{ .Values.storage.object.serviceRef.cluster.name }}
    service:
      component: {{ .Values.storage.object.serviceRef.cluster.component }}
      service: {{ .Values.storage.object.serviceRef.cluster.service }}
      port: {{ .Values.storage.object.serviceRef.cluster.port }}
    {{- if .Values.storage.object.serviceRef.cluster.credential }}
    credential:
      component: {{ .Values.storage.object.serviceRef.cluster.component }}
      name: {{ .Values.storage.object.serviceRef.cluster.credential }}
     {{- end }}
  {{- end }}
  serviceDescriptor: {{ .Values.storage.object.serviceRef.serviceDescriptor }}
{{- end }}
{{- end }}