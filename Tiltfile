load('ext://restart_process', 'docker_build_with_restart')
default_registry("ttl.sh")
docker_build_with_restart("ttl.sh/telepresence-demo-payments-svc:2h", ".", entrypoint="uvicorn app:app --host 0.0.0.0 --port 8080", live_update=[sync("./src", "/app"), sync("./requirements.txt", "/app/requirements.txt")])
k8s_yaml(yaml="k8s/local/deploy.yaml")
k8s_resource(workload="payments-svc", port_forwards=["8080:8080"])
