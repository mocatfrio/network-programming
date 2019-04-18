# File Server
## Tools
1. Python 3
2. Socket 
3. Thread 
4. Asyncore for asynchronous server
5. Linux Operating System

## Description
* There are a **synchronous** server and an **asynchronous** server. The difference is when we execute something synchronously, we wait for it to finish before moving on to another task. In the other hand, when we execute something asynchronously, we can move on to another task before it finishes.
* Server has some features, i.e.:
  * Create a new directory 
  * Delete a directory 
  * Delete a file
  * Move a file or directory
  * List a directory's content
  * Upload a file
  * Download a file
  
## Testing
### synchronous server
1. Run the `sync-server.py`.
   
   ![](img/sync/ss1.png)

2. Create a new directory using `/createdir={directory_name}` URL.

   ![](img/sync/ss2.png)

3. Delete a directory using `/deletedir={directory_name}` URL.
   
   ![](img/sync/ss3.png)

   ![](img/sync/ss4.png)

4. Delete a file using `/delete={file_name_in_the_same_level_with_server_code}` or `/delete={relative_path}/{file_name}` URL.

   ![](img/sync/ss5.png)

   ![](img/sync/ss6.png)

5. Move a file using `/move={source_directory}/{file_name}={destination_directory}` URL.
   
   ![](img/sync/ss7.png)

6. Move a file and rename it using `/move={{source_directory}/{file_name}={destination_directory}/{new_file_name}` URL.

   ![](img/sync/ss8.png)

   ![](img/sync/ss9.png)

7. Move a directory using `/move={source_directory}={destination_directory}` URL.

   ![](img/sync/ss10.png)

8. List the contents of a directory using `/listdir` or `/listdir/{directory_path}` URL.

   ![](img/sync/ss11.png)

   ![](img/sync/ss12.png)

9. Upload a file using `/upload` URL to open the upload form.
    
   ![](img/sync/ss13.png)

   ![](img/sync/ss14.png)

   ![](img/sync/ss15.png)

   ![](img/sync/ss16.png)

10. Last, download a file using `/download={file_name_in_the_same_level_with_server_code}` or `/download={relative_path}/{file_name}` URL.
  
   ![](img/sync/ss17.png)

   ![](img/sync/ss18.png)

### Asynchronous server
1. Run the `async-server.py`.
2. Async-server's features and functionalities are same as the sync-server's, but it's executed asynchronously. These are some proves.
   
   ![](img/async/ss1.png)

   ![](img/async/ss2.png)

   ![](img/async/ss3.png)


   
