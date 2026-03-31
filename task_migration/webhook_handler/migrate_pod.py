import subprocess

def migrate():
    print("Migrating Pod from cloud to edge...")
    subprocess.run(['kubectl', 'delete', 'deployment', 'flask-task-cloud', '-n', 'default'])

    subprocess.run(['kubectl', 'apply', '-f', 'deployment-edge.yaml', '-n', 'default'])
    print("Migration completed.")

if __name__ == "__main__":
    migrate()