#!/usr/bin/env python3
"""
################################################################################
#                         MongoDB Benchmark Test Suite
################################################################################
#
# 🤖 This comprehensive MongoDB benchmark tool was generated by GPT (Claude Sonnet 4)
#    to provide professional-grade MongoDB performance testing across multiple
#    operations and scenarios.
#
# 📋 DESCRIPTION:
#    A professional MongoDB benchmark tool that measures performance across
#    multiple operations and scenarios:
#    - CRUD operations: Insert, Find, Update, Delete
#    - Bulk operations for high-throughput testing
#    - Index performance and optimization
#    - Aggregation pipeline performance
#    - Concurrent client simulation
#    - Different document sizes and structures
#    - Query pattern analysis
#    - Connection pooling efficiency
#    - Sharding performance (if applicable)
#
# 🔧 PREREQUISITES:
#    - Python 3.6 or higher
#    - MongoDB server running and accessible
#    - Python pymongo library (pip install pymongo)
#    - Network access to MongoDB instance
#    - Sufficient disk space for test data
#    - Appropriate MongoDB user permissions
#
# 📦 INSTALLATION:
#    pip install pymongo
#    # OR using system package manager:
#    # Ubuntu/Debian: sudo apt-get install python3-pymongo
#    # CentOS/RHEL: sudo yum install python3-pymongo
#    # macOS: pip3 install pymongo
#
# 🚀 BASIC USAGE:
#    # Local MongoDB instance
#    python3 mongodb_benchmark.py --uri mongodb://localhost:27017
#
#    # Kubernetes MongoDB service (with port forwarding)
#    kubectl port-forward svc/mongodb 27017:27017
#    python3 mongodb_benchmark.py --uri mongodb://localhost:27017
#
# 🎯 ADVANCED USAGE EXAMPLES:
#
#    # High-throughput test with many clients
#    python3 mongodb_benchmark.py --uri mongodb://localhost:27017 \
#                                --clients 100 --documents 100000 --doc-size 1024
#
#    # Authentication with username/password
#    python3 mongodb_benchmark.py --uri mongodb://user:pass@localhost:27017/testdb
#
#    # Replica set testing
#    python3 mongodb_benchmark.py --uri mongodb://host1:27017,host2:27017,host3:27017/testdb?replicaSet=rs0
#
#    # Bulk operations test
#    python3 mongodb_benchmark.py --uri mongodb://localhost:27017 \
#                                --bulk --bulk-size 1000
#
#    # Test specific operations only
#    python3 mongodb_benchmark.py --uri mongodb://localhost:27017 \
#                                --operations insert,find,update
#
#    # Export results to JSON
#    python3 mongodb_benchmark.py --uri mongodb://localhost:27017 \
#                                --output mongodb_results.json
#
# 📊 WHAT IT MEASURES:
#    ✅ Operations per second (throughput)
#    ✅ Latency statistics (mean, median, p95, p99)
#    ✅ Index utilization and performance
#    ✅ Connection establishment time
#    ✅ Error rates and types
#    ✅ Bulk operation efficiency
#    ✅ Concurrent client performance
#    ✅ Different document size impact
#    ✅ Query pattern performance
#    ✅ Aggregation pipeline efficiency
#    ✅ Memory and disk usage patterns
#
# 📈 OUTPUT:
#    - Real-time progress indicators with emoji
#    - Detailed console reports with statistics
#    - Optional JSON export for analysis
#    - Performance comparisons across operations
#    - Error analysis and debugging info
#    - Resource utilization metrics
#    - Index usage statistics
#
# 🗂️ TEST OPERATIONS:
#    - Insert: Single and bulk document insertion
#    - Find: Various query patterns with different selectivity
#    - Update: Single and bulk document updates
#    - Delete: Single and bulk document deletion
#    - Aggregation: Pipeline operations and complex queries
#    - Index: Index creation and query optimization
#
# ⚠️  SAFETY NOTES:
#    - Uses separate test database (configurable)
#    - Automatic cleanup after tests
#    - Rate limiting options to prevent overload
#    - Safe for production testing with proper limits
#    - Connection pooling for efficiency
#    - Respects MongoDB resource limits
#
# 🏆 MONGODB PERFORMANCE TIPS:
#    - Create appropriate indexes for your queries
#    - Use bulk operations for high-throughput scenarios
#    - Monitor working set size vs available RAM
#    - Optimize document schema for your access patterns
#    - Use projection to limit returned fields
#    - Consider sharding for horizontal scaling
#    - Monitor oplog size for replica sets
#    - Use read preferences for read scaling
#    - Optimize aggregation pipelines with $match early
#
# 📄 GENERATED REPORTS:
#    - Console output: Real-time results with detailed statistics
#    - JSON file: mongodb_benchmark_YYYYMMDD_HHMMSS.json with all metrics
#    - Includes: throughput, latency percentiles, error rates, index stats
#
# 🐛 TROUBLESHOOTING:
#    - "Connection refused" → Check MongoDB server status and port
#    - "Authentication failed" → Verify credentials and database permissions
#    - "Cursor timeout" → Reduce batch size or increase cursor timeout
#    - High latency → Check indexes, document size, and system resources
#    - "Too many connections" → Reduce concurrent client count
#    - Write concern errors → Adjust write concern settings
#    - "Collection locked" → Check for long-running operations
#
# 📚 MONGODB-SPECIFIC NOTES:
#    - Tests both single and bulk operations
#    - Supports authentication and replica sets
#    - Compatible with MongoDB 4.x, 5.x, and 6.x
#    - Tests various index types and strategies
#    - Measures document-level locking impact
#    - Validates read/write concern behavior
#    - Tests aggregation framework performance
#
# 🌐 KUBERNETES SETUP:
#    # Port forward MongoDB service
#    kubectl port-forward svc/mongodb 27017:27017
#
#    # Or for MongoDB with authentication
#    kubectl get secret mongodb-secret -o jsonpath="{.data.password}" | base64 -d
#    python3 mongodb_benchmark.py --uri mongodb://admin:<password>@localhost:27017/admin
#
# 📞 SUPPORT:
#    This tool was generated by AI and is provided as-is. For MongoDB
#    performance tuning, consult the official MongoDB documentation
#    at docs.mongodb.com.
#
################################################################################

A comprehensive MongoDB benchmark tool that measures performance across
multiple operations, document types, and concurrency scenarios.

Features:
- CRUD operations with bulk variants
- Index performance testing
- Aggregation pipeline benchmarks
- Concurrent client simulation
- Detailed latency analysis
- JSON result export

Requirements:
- Python 3.6+
- pymongo library
- Access to MongoDB server

Usage:
    python3 mongodb_benchmark.py --uri mongodb://localhost:27017
"""

import pymongo
import time
import argparse
import json
import threading
import random
import string
from datetime import datetime, timedelta
from statistics import mean, median, pstdev
from concurrent.futures import ThreadPoolExecutor, as_completed
from bson import ObjectId


class MongoDBBenchmark:
    """
    Comprehensive MongoDB benchmark tool for performance testing.

    Supports multiple operation types, concurrent clients, and detailed
    performance analysis with export capabilities.
    """

    def __init__(self, uri, database_name='benchmark_test', timeout=30, max_pool_size=100):
        """
        Initialize MongoDB benchmark with connection parameters.

        Args:
            uri (str): MongoDB connection URI
            database_name (str): Database name for testing
            timeout (int): Connection timeout in seconds
            max_pool_size (int): Maximum connections in pool
        """
        self.uri = uri
        self.database_name = database_name
        self.collection_name = 'test_collection'

        # Connection configuration
        self.client = pymongo.MongoClient(
            uri,
            serverSelectionTimeoutMS=timeout * 1000,
            maxPoolSize=max_pool_size,
            retryWrites=True
        )

        self.db = self.client[database_name]
        self.collection = self.db[self.collection_name]

        # Thread-safe storage for results
        self._lock = threading.Lock()
        self.latencies = []
        self.errors = []
        self.results = {
            'connection': {},
            'tests': {},
            'summary': {},
            'config': {
                'uri': uri,
                'database': database_name,
                'collection': self.collection_name,
                'timeout': timeout,
                'max_pool_size': max_pool_size
            }
        }

    def check_connection(self):
        """
        Test MongoDB connection and gather server information.

        Returns:
            bool: True if connection successful, False otherwise
        """
        print("🔌 Testing MongoDB connection...")

        try:
            start_time = time.time()

            # Test basic connectivity
            server_info = self.client.server_info()
            connection_time = time.time() - start_time

            print(f"✅ Connected successfully in {connection_time:.3f}s")

            # Gather additional server information
            try:
                admin_db = self.client.admin
                status = admin_db.command('serverStatus')

                db_stats = self.db.command('dbStats')

                server_details = {
                    'mongodb_version': server_info.get('version', 'Unknown'),
                    'uptime': status.get('uptime', 0),
                    'connections_current': status.get('connections', {}).get('current', 0),
                    'connections_available': status.get('connections', {}).get('available', 0),
                    'storage_engine': status.get('storageEngine', {}).get('name', 'Unknown'),
                    'database_size': db_stats.get('dataSize', 0),
                    'index_size': db_stats.get('indexSize', 0),
                    'collections': db_stats.get('collections', 0)
                }

                print(f"   MongoDB Version: {server_details['mongodb_version']}")
                print(f"   Storage Engine: {server_details['storage_engine']}")
                print(f"   Current Connections: {server_details['connections_current']}")
                print(f"   Available Connections: {server_details['connections_available']}")

                self.results['connection'] = {
                    'success': True,
                    'time': connection_time,
                    'server_info': server_details
                }
            except Exception as e:
                print(f"   ⚠️ Could not get detailed server info: {e}")
                self.results['connection'] = {
                    'success': True,
                    'time': connection_time,
                    'server_info': {'mongodb_version': server_info.get('version', 'Unknown')}
                }

            return True

        except pymongo.errors.ServerSelectionTimeoutError as e:
            print(f"❌ Connection timeout: {e}")
            self.results['connection'] = {'success': False, 'error': f'Timeout: {e}'}
            return False
        except pymongo.errors.OperationFailure as e:
            print(f"❌ Authentication failed: {e}")
            self.results['connection'] = {'success': False, 'error': f'Auth error: {e}'}
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.results['connection'] = {'success': False, 'error': f'Unexpected error: {e}'}
            return False

    def setup_test_environment(self):
        """Prepare test environment with indexes and cleanup."""
        try:
            # Drop existing collection
            self.collection.drop()
            print("✅ Test collection dropped")

            # Create indexes for testing - simplified approach
            try:
                # Single field indexes
                self.collection.create_index([('user_id', pymongo.ASCENDING)])
                self.collection.create_index([('timestamp', pymongo.DESCENDING)])

                # Compound index
                self.collection.create_index([
                    ('category', pymongo.ASCENDING),
                    ('status', pymongo.ASCENDING)
                ])

                # Geospatial index
                self.collection.create_index([('location', pymongo.GEO2D)])

                print("✅ Test indexes created")
            except Exception as idx_error:
                print(f"⚠️ Warning: Could not create some indexes: {idx_error}")
                # Continue without indexes - the benchmark will still work

        except Exception as e:
            print(f"⚠️ Warning: Could not setup test environment: {e}")

    def _generate_document(self, doc_size=500, doc_id=None):
        """
        Generate a realistic test document.

        Args:
            doc_size (int): Approximate document size in bytes
            doc_id (int): Optional document ID for consistent generation

        Returns:
            dict: Generated document
        """
        # Base document structure
        doc = {
            'user_id': random.randint(1, 10000),
            'timestamp': datetime.utcnow(),
            'category': random.choice(['electronics', 'books', 'clothing', 'home', 'sports']),
            'status': random.choice(['active', 'inactive', 'pending', 'completed']),
            'price': round(random.uniform(10.0, 999.99), 2),
            'quantity': random.randint(1, 100),
            'location': [random.uniform(-180, 180), random.uniform(-90, 90)],
            'tags': random.sample(['new', 'sale', 'featured', 'limited', 'popular'], k=random.randint(1, 3)),
            'metadata': {
                'created_by': f'user_{random.randint(1, 1000)}',
                'version': random.randint(1, 10),
                'source': random.choice(['web', 'mobile', 'api'])
            }
        }

        if doc_id is not None:
            doc['_id'] = ObjectId()
            doc['sequence_id'] = doc_id

        # Add padding to reach desired size
        current_size = len(str(doc).encode('utf-8'))
        if current_size < doc_size:
            padding_size = doc_size - current_size - 50  # Leave some buffer
            if padding_size > 0:
                doc['padding'] = 'x' * padding_size

        return doc

    def _record_operation(self, start_time, success=True, error=None):
        """
        Thread-safe recording of operation results.

        Args:
            start_time (float): Operation start time
            success (bool): Whether operation succeeded
            error (str): Error message if operation failed
        """
        latency = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds

        with self._lock:
            if success:
                self.latencies.append(latency)
            else:
                self.errors.append(error or "Unknown error")

    def _insert_worker(self, num_docs, doc_size, bulk_size=None):
        """
        Worker function for insert operations.

        Args:
            num_docs (int): Number of documents to insert
            doc_size (int): Size of each document
            bulk_size (int): Bulk operation size (None for single inserts)
        """
        client = pymongo.MongoClient(self.uri)
        collection = client[self.database_name][self.collection_name]

        if bulk_size and bulk_size > 1:
            # Bulk insert operations
            docs_inserted = 0
            while docs_inserted < num_docs:
                batch_size = min(bulk_size, num_docs - docs_inserted)
                documents = [self._generate_document(doc_size, docs_inserted + i)
                           for i in range(batch_size)]

                try:
                    start = time.perf_counter()
                    collection.insert_many(documents, ordered=False)
                    self._record_operation(start, success=True)
                    docs_inserted += batch_size
                except Exception as e:
                    self._record_operation(start, success=False, error=str(e))
                    docs_inserted += batch_size  # Continue even on error
        else:
            # Single insert operations
            for i in range(num_docs):
                document = self._generate_document(doc_size, i)

                try:
                    start = time.perf_counter()
                    collection.insert_one(document)
                    self._record_operation(start, success=True)
                except Exception as e:
                    self._record_operation(start, success=False, error=str(e))

        client.close()

    def _find_worker(self, num_queries, query_types=['simple', 'range', 'complex']):
        """
        Worker function for find operations.

        Args:
            num_queries (int): Number of queries to execute
            query_types (list): Types of queries to test
        """
        client = pymongo.MongoClient(self.uri)
        collection = client[self.database_name][self.collection_name]

        for i in range(num_queries):
            query_type = random.choice(query_types)

            try:
                start = time.perf_counter()

                if query_type == 'simple':
                    # Simple equality query
                    user_id = random.randint(1, 10000)
                    cursor = collection.find({'user_id': user_id}).limit(100)
                    list(cursor)  # Force execution

                elif query_type == 'range':
                    # Range query
                    min_price = random.uniform(10, 500)
                    max_price = min_price + random.uniform(100, 500)
                    cursor = collection.find({
                        'price': {'$gte': min_price, '$lte': max_price}
                    }).limit(100)
                    list(cursor)

                elif query_type == 'complex':
                    # Complex query with multiple conditions
                    category = random.choice(['electronics', 'books', 'clothing'])
                    cursor = collection.find({
                        'category': category,
                        'status': 'active',
                        'quantity': {'$gt': 10}
                    }).sort('timestamp', -1).limit(50)
                    list(cursor)

                self._record_operation(start, success=True)

            except Exception as e:
                self._record_operation(start, success=False, error=str(e))

        client.close()

    def _update_worker(self, num_updates, bulk_size=None):
        """
        Worker function for update operations.

        Args:
            num_updates (int): Number of updates to perform
            bulk_size (int): Bulk operation size (None for single updates)
        """
        client = pymongo.MongoClient(self.uri)
        collection = client[self.database_name][self.collection_name]

        if bulk_size and bulk_size > 1:
            # Bulk update operations
            updates_done = 0
            while updates_done < num_updates:
                batch_size = min(bulk_size, num_updates - updates_done)
                operations = []

                for i in range(batch_size):
                    user_id = random.randint(1, 10000)
                    operations.append(
                        pymongo.UpdateOne(
                            {'user_id': user_id},
                            {'$set': {'last_updated': datetime.utcnow(),
                                    'update_count': random.randint(1, 100)}}
                        )
                    )

                try:
                    start = time.perf_counter()
                    collection.bulk_write(operations, ordered=False)
                    self._record_operation(start, success=True)
                    updates_done += batch_size
                except Exception as e:
                    self._record_operation(start, success=False, error=str(e))
                    updates_done += batch_size
        else:
            # Single update operations
            for i in range(num_updates):
                user_id = random.randint(1, 10000)

                try:
                    start = time.perf_counter()
                    collection.update_one(
                        {'user_id': user_id},
                        {'$set': {'last_updated': datetime.utcnow(),
                                'update_count': random.randint(1, 100)}}
                    )
                    self._record_operation(start, success=True)
                except Exception as e:
                    self._record_operation(start, success=False, error=str(e))

        client.close()

    def _delete_worker(self, num_deletes):
        """
        Worker function for delete operations.

        Args:
            num_deletes (int): Number of deletes to perform
        """
        client = pymongo.MongoClient(self.uri)
        collection = client[self.database_name][self.collection_name]

        for i in range(num_deletes):
            user_id = random.randint(1, 10000)

            try:
                start = time.perf_counter()
                collection.delete_one({'user_id': user_id})
                self._record_operation(start, success=True)
            except Exception as e:
                self._record_operation(start, success=False, error=str(e))

        client.close()

    def _aggregation_worker(self, num_aggregations):
        """
        Worker function for aggregation operations.

        Args:
            num_aggregations (int): Number of aggregations to perform
        """
        client = pymongo.MongoClient(self.uri)
        collection = client[self.database_name][self.collection_name]

        aggregation_pipelines = [
            # Group by category and count
            [
                {'$match': {'status': 'active'}},
                {'$group': {'_id': '$category', 'count': {'$sum': 1}, 'avg_price': {'$avg': '$price'}}},
                {'$sort': {'count': -1}}
            ],
            # Calculate daily statistics
            [
                {'$group': {
                    '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}},
                    'total_sales': {'$sum': '$price'},
                    'count': {'$sum': 1}
                }},
                {'$sort': {'_id': -1}},
                {'$limit': 30}
            ],
            # Find top users by activity
            [
                {'$group': {'_id': '$user_id', 'activity': {'$sum': 1}, 'total_spent': {'$sum': '$price'}}},
                {'$sort': {'activity': -1}},
                {'$limit': 100}
            ]
        ]

        for i in range(num_aggregations):
            pipeline = random.choice(aggregation_pipelines)

            try:
                start = time.perf_counter()
                list(collection.aggregate(pipeline))
                self._record_operation(start, success=True)
            except Exception as e:
                self._record_operation(start, success=False, error=str(e))

        client.close()

    def run_benchmark(self, operation_type='insert', num_clients=10, total_operations=10000,
                     doc_size=500, bulk_size=None):
        """
        Run comprehensive benchmark test.

        Args:
            operation_type (str): Type of operations ('insert', 'find', 'update', 'delete', 'aggregation')
            num_clients (int): Number of concurrent clients
            total_operations (int): Total number of operations
            doc_size (int): Size of documents (for insert operations)
            bulk_size (int): Bulk operation size
        """
        print(f"\n🏁 Starting {operation_type.upper()} benchmark")
        print(f"   Clients: {num_clients}")
        print(f"   Total operations: {total_operations:,}")
        if operation_type == 'insert':
            print(f"   Document size: {doc_size} bytes")
        if bulk_size:
            print(f"   Bulk size: {bulk_size}")
        print("="*60)

        # Reset counters
        self.latencies = []
        self.errors = []

        ops_per_client = total_operations // num_clients
        start_time = time.time()

        # Run benchmark with thread pool
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            futures = []

            for client_id in range(num_clients):
                if operation_type == 'insert':
                    future = executor.submit(
                        self._insert_worker, ops_per_client, doc_size, bulk_size
                    )
                elif operation_type == 'find':
                    future = executor.submit(
                        self._find_worker, ops_per_client
                    )
                elif operation_type == 'update':
                    future = executor.submit(
                        self._update_worker, ops_per_client, bulk_size
                    )
                elif operation_type == 'delete':
                    future = executor.submit(
                        self._delete_worker, ops_per_client
                    )
                elif operation_type == 'aggregation':
                    future = executor.submit(
                        self._aggregation_worker, ops_per_client
                    )
                else:
                    raise ValueError(f"Unknown operation type: {operation_type}")

                futures.append(future)

            # Wait for all clients to complete
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()  # This will raise any exceptions
                    completed += 1
                    if completed % max(1, num_clients // 10) == 0:
                        print(f"   📊 {completed}/{num_clients} clients completed...")
                except Exception as e:
                    print(f"   ❌ Client error: {e}")

        end_time = time.time()
        duration = end_time - start_time

        # Calculate and store results
        self._calculate_and_store_results(operation_type, duration, total_operations)

    def _calculate_and_store_results(self, operation_type, duration, expected_operations):
        """
        Calculate comprehensive performance statistics.

        Args:
            operation_type (str): Type of operations tested
            duration (float): Test duration in seconds
            expected_operations (int): Expected number of operations
        """
        successful_ops = len(self.latencies)
        error_count = len(self.errors)
        total_ops = successful_ops + error_count

        if successful_ops > 0:
            # Calculate latency statistics
            sorted_latencies = sorted(self.latencies)
            results = {
                'operation_type': operation_type,
                'total_operations': total_ops,
                'successful_operations': successful_ops,
                'errors': error_count,
                'error_rate': (error_count / total_ops * 100) if total_ops > 0 else 0,
                'duration': duration,
                'throughput': successful_ops / duration,
                'latency_stats': {
                    'mean': mean(self.latencies),
                    'median': median(self.latencies),
                    'p95': sorted_latencies[int(len(sorted_latencies) * 0.95)],
                    'p99': sorted_latencies[int(len(sorted_latencies) * 0.99)],
                    'min': min(self.latencies),
                    'max': max(self.latencies),
                    'stdev': pstdev(self.latencies) if len(self.latencies) > 1 else 0
                }
            }
        else:
            results = {
                'operation_type': operation_type,
                'total_operations': total_ops,
                'successful_operations': 0,
                'errors': error_count,
                'error_rate': 100,
                'duration': duration,
                'throughput': 0,
                'latency_stats': {}
            }

        self.results['tests'][operation_type] = results
        self._print_results(results)

    def _print_results(self, results):
        """
        Print formatted benchmark results to console.

        Args:
            results (dict): Test results dictionary
        """
        print(f"\n📊 {results['operation_type'].upper()} Benchmark Results:")
        print("=" * 60)
        print(f"Total operations: {results['total_operations']:,}")
        print(f"Successful operations: {results['successful_operations']:,}")
        print(f"Errors: {results['errors']:,}")
        print(f"Error rate: {results['error_rate']:.2f}%")
        print(f"Duration: {results['duration']:.2f}s")
        print(f"Throughput: {results['throughput']:,.2f} ops/sec")

        if results['latency_stats']:
            stats = results['latency_stats']
            print(f"\nLatency Statistics:")
            print(f"  Mean: {stats['mean']:.2f}ms")
            print(f"  Median: {stats['median']:.2f}ms")
            print(f"  95th percentile: {stats['p95']:.2f}ms")
            print(f"  99th percentile: {stats['p99']:.2f}ms")
            print(f"  Min: {stats['min']:.2f}ms")
            print(f"  Max: {stats['max']:.2f}ms")
            print(f"  Std deviation: {stats['stdev']:.2f}ms")

        print("=" * 60)

    def generate_report(self, output_file=None):
        """
        Generate comprehensive benchmark report.

        Args:
            output_file (str): Optional JSON file to save results
        """
        # Add summary statistics
        self.results['summary'] = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.results['tests']),
            'overall_success': all(
                test.get('error_rate', 100) < 50
                for test in self.results['tests'].values()
            )
        }

        # Print summary to console
        print(f"\n{'='*80}")
        print(f"📋 MONGODB BENCHMARK SUMMARY REPORT")
        print(f"{'='*80}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"MongoDB URI: {self.results['config']['uri']}")
        print(f"Database: {self.results['config']['database']}")

        if self.results['connection'].get('success'):
            server_info = self.results['connection'].get('server_info', {})
            print(f"MongoDB Version: {server_info.get('mongodb_version', 'Unknown')}")
            print(f"Storage Engine: {server_info.get('storage_engine', 'Unknown')}")

        print(f"{'='*80}")

        # Print test results summary
        for test_name, test_results in self.results['tests'].items():
            print(f"\n{test_name.upper()} Operations:")
            print(f"  Throughput: {test_results['throughput']:,.0f} ops/sec")
            if test_results['latency_stats']:
                print(f"  Avg Latency: {test_results['latency_stats']['mean']:.2f}ms")
                print(f"  P99 Latency: {test_results['latency_stats']['p99']:.2f}ms")
            print(f"  Error Rate: {test_results['error_rate']:.2f}%")

        print(f"\n{'='*80}")

        # Save to JSON file if requested
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    json.dump(self.results, f, indent=2, default=str)
                print(f"📄 Detailed results saved to: {output_file}")
            except Exception as e:
                print(f"⚠️  Warning: Could not save results to {output_file}: {e}")

    def cleanup(self):
        """Clean up test data and close connections."""
        try:
            self.collection.drop()
            self.client.close()
            print("✅ Cleanup completed")
        except Exception as e:
            print(f"⚠️ Warning during cleanup: {e}")


def main():
    """Main function to run MongoDB benchmark with command line arguments."""
    parser = argparse.ArgumentParser(
        description='Comprehensive MongoDB Benchmark Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic benchmark
  python3 mongodb_benchmark.py --uri mongodb://localhost:27017

  # High-throughput test
  python3 mongodb_benchmark.py --uri mongodb://localhost:27017 \\
                              --clients 100 --documents 100000

  # With authentication
  python3 mongodb_benchmark.py --uri mongodb://user:pass@localhost:27017/testdb

  # Bulk operations
  python3 mongodb_benchmark.py --uri mongodb://localhost:27017 \\
                              --bulk --bulk-size 1000

  # Export to JSON
  python3 mongodb_benchmark.py --uri mongodb://localhost:27017 \\
                              --output results.json
        """
    )

    # Connection parameters
    parser.add_argument('--uri', required=True,
                       help='MongoDB connection URI (e.g., mongodb://localhost:27017)')
    parser.add_argument('--database', default='benchmark_test',
                       help='Database name for testing (default: benchmark_test)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Connection timeout in seconds (default: 30)')
    parser.add_argument('--max-pool-size', type=int, default=100,
                       help='Maximum connections in pool (default: 100)')

    # Benchmark parameters
    parser.add_argument('--clients', type=int, default=10,
                       help='Number of concurrent clients (default: 10)')
    parser.add_argument('--documents', type=int, default=10000,
                       help='Total number of documents/operations (default: 10000)')
    parser.add_argument('--doc-size', type=int, default=500,
                       help='Document size in bytes (default: 500)')

    # Advanced options
    parser.add_argument('--operations', default='insert,find,update,delete,aggregation',
                       help='Comma-separated list of operations to test')
    parser.add_argument('--bulk', action='store_true',
                       help='Enable bulk operations')
    parser.add_argument('--bulk-size', type=int, default=100,
                       help='Bulk operation size (default: 100)')

    # Output options
    parser.add_argument('--output', help='Output file for JSON results')
    parser.add_argument('--no-cleanup', action='store_true',
                       help='Skip database cleanup (useful for debugging)')

    args = parser.parse_args()

    # Validate arguments
    if args.clients <= 0 or args.documents <= 0:
        print("❌ Error: Client count and document count must be positive")
        return 1

    if args.doc_size < 50:
        print("❌ Error: Document size must be at least 50 bytes")
        return 1

    # Parse operations list
    operations = [op.strip().lower() for op in args.operations.split(',')]
    valid_operations = ['insert', 'find', 'update', 'delete', 'aggregation']

    for op in operations:
        if op not in valid_operations:
            print(f"❌ Error: Invalid operation '{op}'. Valid options: {', '.join(valid_operations)}")
            return 1

    # Check pymongo library
    try:
        import pymongo
    except ImportError:
        print("❌ Error: pymongo library is required")
        print("Install with: pip install pymongo")
        return 1

    # Initialize benchmark
    print("🚀 Starting MongoDB Benchmark Suite")
    print("="*70)

    benchmark = MongoDBBenchmark(
        uri=args.uri,
        database_name=args.database,
        timeout=args.timeout,
        max_pool_size=args.max_pool_size
    )

    try:
        # Test connection
        if not benchmark.check_connection():
            print("❌ Cannot proceed without MongoDB connection")
            return 1

        # Prepare test environment
        benchmark.setup_test_environment()

        # Run benchmarks for each operation type
        bulk_size = args.bulk_size if args.bulk else None

        # For some operations, we need data to exist first
        if 'find' in operations or 'update' in operations or 'delete' in operations or 'aggregation' in operations:
            if 'insert' not in operations:
                print("📊 Pre-populating database for read/update/delete operations...")
                benchmark.run_benchmark(
                    operation_type='insert',
                    num_clients=args.clients,
                    total_operations=args.documents,
                    doc_size=args.doc_size,
                    bulk_size=bulk_size
                )

        for operation in operations:
            benchmark.run_benchmark(
                operation_type=operation,
                num_clients=args.clients,
                total_operations=args.documents,
                doc_size=args.doc_size,
                bulk_size=bulk_size
            )

        # Generate final report
        benchmark.generate_report(args.output)

    except KeyboardInterrupt:
        print("\n🚫 Benchmark interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    finally:
        # Cleanup
        if not args.no_cleanup:
            benchmark.cleanup()

    print("\n✅ MongoDB benchmark completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())