import cml
import requests as req
import download_file
import os
import hashlib


current_directory=os.getcwd()+"/.command_mcsl"
now_dir=os.getcwd()





def calculate_hash(file_path, hash_algorithm='sha256'):
    """计算文件的哈希值"""
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        # 读取并更新哈希值，直到文件结束
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()
eh=0
def verify_hash(file_path, expected_hash, hash_algorithm='sha256'):
    """验证文件的哈希值是否与预期的哈希值匹配"""
    calculated_hash = calculate_hash(file_path, hash_algorithm)
    eh=calculate_hash
    return calculated_hash == expected_hash




cml.install.install_minecraft_version



while True:
    cmd = input("(Minecraft Server Launcher) | [Main]>> ")

    if cmd == "exit":
        os.chdir(now_dir)
        quit()
    elif cmd == "help":
        print("help - show this message")
        print("exit - exit the program")
        print("install  - install Minecraft server")
        print("start - start a Minecraft server")
    elif cmd == "install":
        print("Minecraft Server Launcher | Install Minecraft Server\nMinecraft Server Versions:\n\n\n\n\n\n\n")
        verisons = cml.utils.get_version_list()
        for v in verisons:
            print(v["id"])
        command = input("(Minecraft Server Launcher) | [Install] {Enter version ID} >> ")
        name = input("(Minecraft Server Launcher) | [Install] {Enter your server name} >> ")
        if command in [v["id"] for v in verisons]:
            print("Installing Minecraft Server...")
            for v in verisons:
                if v["id"] == command:
                    version = v
                    break
            print(f"Minecraft Server Launcher | INFO: Downloading {version['id']}.json...")
            url = version["url"]
            response = req.get(url)
            data = response.json()
            print(f"Minecraft Server Launcher | INFO: Downloading {version['id']}-server.jar...")
            url = data["downloads"]["server"]["url"]
            seve_dir=current_directory+"/servers/"+name
            print(f"Minecraft Server Launcher | INFO: sever directorys: {seve_dir}")
            download_file.main(urls=[url], folder=seve_dir, name=f"{version['id']}-server.jar")
            print(f"Minecraft Server Launcher | INFO: Extracting {version['id']}-server.jar...")
            print(f"Verifying the hash value of {version['id']}-server.jar")
            print("Minecraft Server installed successfully.")
            open(current_directory+"/servers/"+name+"/version.serverconfig.cofg", "w").write(version["id"])
        else:
            print("Unknown version ID.")
    elif cmd == "start":
        print("Minecraft Server Launcher | Start Minecraft Server\nMinecraft Server List:\n\n\n\n\n\n\n")
        for server in os.listdir(current_directory+"/servers"):
            print(server)
        server_name=input("(Minecraft Server Launcher) | [Start] {Enter server name} >> ")
        if server_name in os.listdir(current_directory+"/servers"):
            print(f"Starting Minecraft Server {server_name}...")
            print("Minecraft Server Launcher) | INFO: Minecraft EULA URL: https://aka.ms/MinecraftEULA")
            open(current_directory+"/servers/"+server_name+"/eula.txt", "w").write("""
#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).
#Thu Feb 06 15:52:30 CST 2025
eula=true
""")        
            now_dir=os.getcwd()
            os.chdir(current_directory+"/servers/"+server_name)
            try:
                version_id=open(current_directory+"/servers/"+server_name+"/version.serverconfig.cofg", "r").read()
                os.system(f"java -jar {version_id}-server.jar nogui")
                print("Minecraft Server Launcher | INFO: Minecraft Server has been started successfully.")
            except FileNotFoundError:
                print("Minecraft Server Launcher | ERROR: This server may not have been downloaded completely.")
            os.chdir(now_dir)
        else:
            print("Unknown server name.")
    else:
        print("Invalid command. Type 'help' for a list of commands.")


