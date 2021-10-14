from server_helper import server_helper


if __name__ == "__main__":
    server = server_helper(web_path="./webroot")

    server.listen()
