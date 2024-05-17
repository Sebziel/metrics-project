#sudo python3 server.py > /dev/null 2>&1 &

from http.server import BaseHTTPRequestHandler, HTTPServer
import random

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, 'utf8'))

    def do_GET(self):
        if self.path == '/metrics':
            heap_memory = random.randint(10**8, 10**10)
            nonheap_memory = random.randint(10**8, 10**10)
            code_cache_memory = random.randint(10**7, 10**9)
            metaspace_memory = random.randint(10**7, 10**9)
            compressed_class_space_memory = random.randint(10**7, 10**9)
            ps_eden_space_memory = random.randint(10**7, 10**9)
            ps_survivor_space_memory = random.randint(10**7, 10**9)
            ps_old_gen_memory = random.randint(10**7, 10**9)

            metrics = f'# HELP jvm_memory_bytes_used Used bytes of a given JVM memory area.\n' \
                       f'# TYPE jvm_memory_bytes_used gauge\n' \
                       f'jvm_memory_bytes_used{{area="heap",}} {heap_memory}\n' \
                       f'jvm_memory_bytes_used{{area="nonheap",}} {nonheap_memory}\n' \
                       f'# HELP jvm_memory_pool_bytes_used Used bytes of a given JVM memory pool.\n' \
                       f'# TYPE jvm_memory_pool_bytes_used gauge\n' \
                       f'jvm_memory_pool_bytes_used{{pool="Code Cache",}} {code_cache_memory}\n' \
                       f'jvm_memory_pool_bytes_used{{pool="Metaspace",}} {metaspace_memory}\n' \
                       f'jvm_memory_pool_bytes_used{{pool="Compressed Class Space",}} {compressed_class_space_memory}\n' \
                       f'jvm_memory_pool_bytes_used{{pool="PS Eden Space",}} {ps_eden_space_memory}\n' \
                       f'jvm_memory_pool_bytes_used{{pool="PS Survivor Space",}} {ps_survivor_space_memory}\n' \
                       f'jvm_memory_pool_bytes_used{{pool="PS Old Gen",}} {ps_old_gen_memory}\n'
            self._send_response(metrics)
        elif self.path == '/metrics/gc':
            gc_ps_scavenge_count = random.randint(10**4, 10**5)
            gc_ps_marksweep_count = random.randint(10**1, 10**3)
            gc_ps_scavenge_sum = random.randint(10**2, 10**4)
            gc_ps_marksweep_sum = random.randint(10**2, 10**4)
            metrics = f'# HELP jvm_gc_collection_seconds Time spent in a given JVM garbage collector in seconds.\n' \
                        f'# TYPE jvm_gc_collection_seconds summary\n' \
                        f'jvm_gc_collection_seconds_count{{gc="PS Scavenge",}} {gc_ps_scavenge_count}\n' \
                        f'jvm_gc_collection_seconds_count{{gc="PS MarkSweep",}} {gc_ps_marksweep_count}\n' \
                        f'jvm_gc_collection_seconds_sum{{gc="PS Scavenge",}} {gc_ps_scavenge_sum}\n' \
                        f'jvm_gc_collection_seconds_sum{{gc="PS MarkSweep",}} {gc_ps_marksweep_sum}\n'
            self._send_response(metrics)
        else:
            self._send_response('Not found, probably an incorrect url have been provided. Make sure to append the endpoint to /metrics!')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()