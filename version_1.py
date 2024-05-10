import pathlib
from queue import Queue
from threading import Thread
import logging
import time
import random

class FileProcessor:
    def __init__(self, files, keywords, results_queue):
        self.files = files
        self.keywords = keywords
        self.results_queue = results_queue

    def process(self):
        results = {}
        start_time = time.time()  
        for file_path in self.files:
            logging.info(f"Processing file {file_path.name}")
            found_keywords = self.search_keywords_in_file(file_path)
            results[file_path.name] = found_keywords

            time.sleep(random.uniform(0, 1))
        self.results_queue.put(results)
        end_time = time.time() 
        logging.info(f"Processing time: {end_time - start_time:.2f} seconds")

    def search_keywords_in_file(self, file_path):
        found_keywords = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in self.keywords:
                    if keyword in content:
                        found_keywords.append(keyword)
        except Exception as e:
            logging.error(f"Error processing file {file_path.name}: {e}")
        return found_keywords

def main():
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    keywords = ["first", "second", "third"]  
    results_queue = Queue() 

    list_files = list(pathlib.Path("files").glob("*.txt"))  
    num_threads = 3 

    files_per_thread = len(list_files) // num_threads
    threads = []
    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = (i + 1) * files_per_thread if i < num_threads - 1 else len(list_files)
        files_slice = list_files[start_index:end_index]
        processor = FileProcessor(files_slice, keywords, results_queue)
        thread = Thread(target=processor.process)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    results = {}
    while not results_queue.empty():
        results.update(results_queue.get())

    print("Results:")
    for file_name, found_keywords in results.items():
        print(f"File: {file_name}, Keywords found: {', '.join(found_keywords)}")

if __name__ == "__main__":
    main()