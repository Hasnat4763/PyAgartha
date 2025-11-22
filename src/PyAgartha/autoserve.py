import sys
import subprocess
import time



def autoserve(module_name, port=8080, autoreload=False):        
    child = None
    def run_server():
        subprocess.run([sys.executable, "-m", "waitress", "--port", str(port), f"{module_name}:app"])
        
    if not autoreload:
        run_server()
    else:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class ReloadHandler(FileSystemEventHandler):
            def on_modified(self, event):
                nonlocal child
                event.src_path = str(event.src_path)
                
                if (event.src_path.endswith(".py") or event.src_path.endswith(".html") or event.src_path.endswith(".css")) and 'venv' not in event.src_path and "__pycache__" not in event.src_path:
                    print(f"Detected change in {event.src_path}. Restarting server...")
                    if child:
                        child.terminate()
                        child.wait()
                        time.sleep(0.5)
        observer = Observer()
        observer.schedule(ReloadHandler(), path=".", recursive=True)
        observer.start()

        while True:
            child = subprocess.Popen([sys.executable, "-m", "waitress", "--port", str(port), f"{module_name}:app"])
            try:
                child.wait()
            except KeyboardInterrupt:
                child.terminate()
                break

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("module", help="Module to serve, like app")
    parser.add_argument("--port", type=int, default=8080, help="Port on the server will serve on")
    parser.add_argument("--autoreload", action="store_true")
    args = parser.parse_args()
    autoserve(args.module, port=args.port, autoreload=args.autoreload)