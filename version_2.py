import os
import multiprocessing
from queue import Queue

def search_in_file(file_path, keywords, result_queue):
    found_in_file = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            for keyword in keywords:
                if keyword in line:
                    if keyword in found_in_file:
                        found_in_file[keyword].append((os.path.basename(file_path), line_number))
                    else:
                        found_in_file[keyword] = [(os.path.basename(file_path), line_number)]
    if found_in_file:
        result_queue.put(found_in_file)

def process_files(file_list, keywords, result_queue):
    for file_path in file_list:
        search_in_file(file_path, keywords, result_queue)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = [
        os.path.join(base_dir, "files", "file1.txt"),
        os.path.join(base_dir, "files", "file2.txt"),
        os.path.join(base_dir, "files", "file3.txt")
        ]
    
    keywords = ["first", "second", "third"]
    result_queue = multiprocessing.Queue()

    num_processes = multiprocessing.cpu_count()
    files_per_process = len(files) // num_processes
    processes = []

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = start_index + files_per_process if i < num_processes - 1 else len(files)
        process = multiprocessing.Process(target=process_files, args=(files[start_index:end_index], keywords, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = {}
    while not result_queue.empty():
        result = result_queue.get()
        for key, value in result.items():
            if key in results:
                results[key].extend(value)
            else:
                results[key] = value

    print("Results:")
    for key, value in results.items():
        for file_path in value:
            print(f"File: {file_path}, Keywords found: {key}")   

if __name__ == "__main__":
    main()


