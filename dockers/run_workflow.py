import argparse
import docker
import time
import os


DEFAULT_OUTPUT_PATH = "~/ml_matchers/DLMatchers/dockers/mostmatchers/output/"
DEFAULT_SCRIPT_PATH = "~/ml_matchers/DLMatchers/dockers/mostmatchers/scripts/"

pyjedai_arguments = {
}

magellan_arguments = {
}

algorithm_arguments = {
    "pyjedai" : pyjedai_arguments,
    "magellan" : magellan_arguments
}

conda_env = {
    "pyjedai" : "p39",
    "magellan": "p37"
}

def arguments_to_dict(environment_arguments : dict, script_arguments : dict):
    environment_dict = vars(environment_arguments)
    script_dict = {}
    
    for script_argument in script_arguments:
        argument_name, argument_value = script_argument.lstrip('--').split('=', 1)
        script_dict[argument_name] = argument_value
           
    return environment_dict, script_dict

def generate_output_path(algorithm : str):
    return f"{DEFAULT_OUTPUT_PATH}{algorithm}_out.txt"

def generate_script_path(algorithm : str):
    return f"{DEFAULT_SCRIPT_PATH}{algorithm}.py"

def initialize_file(file_path : str):
    if os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
        print(f"File at '{file_path}' exists - Cleaning up its contents.")
    else:
        with open(file_path, 'w') as file:
            print(f"File created at '{file_path}'.")

def run_script_in_docker(algorithm : str,
                        output_path : str,
                        script_path : str,
                        source_path : str,
                        target_path :str,
                        gt_path : str,
                        arguments : dict):

    client = docker.from_env()
    image_tag = f"{algorithm}"
    try:
        client.images.get(image_tag)
        print(f"Retrieved Docker Image: {image_tag}")
    except docker.errors.ImageNotFound:
        print(f"Building Docker Image: {image_tag}")
        client.images.build(path='.', tag=image_tag)
        
    command = []
    for argument, value in arguments.items():
        command.append(f"--{str(argument)}")
        command.append(f"{str(value)}")
    volumes={
        script_path: {'bind': '/app/script.py', 'mode': 'ro'},
        output_path: {'bind': '/app/output.txt', 'mode': 'rw'},
        source_path: {'bind': '/app/source.csv', 'mode': 'rw'},
        gt_path: {'bind': '/app/gt.csv', 'mode': 'rw'}
    }
    
    if target_path is not None:
        volumes[target_path] = {'bind': '/app/target.csv', 'mode': 'rw'}
    
    initialize_file(file_path=output_path)
    container = client.containers.run(
        image=image_tag,
        command=["conda", "run", "--name", conda_env[algorithm], "python", "/app/script.py"] + command,
        # command=["tail", "-f", "/dev/null"],
        remove=False,
        detach=False,
        tty=True,
        stdin_open=True,
        stdout=True,
        volumes=volumes
    )
    
    # container.wait()
    # output = container.logs().decode('utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorithm script's arguments")
    parser.add_argument("--algorithm", type=str, required=True, help="Algorithm Name")
    parser.add_argument("--source-path", type=str, required=True, help="Path to source dataset")
    parser.add_argument("--gt-path", type=str, required=True, help="Path to ground truth")
    parser.add_argument("--target-path", type=str, help="Path to target dataset")
    parser.add_argument("--output-path", type=str, help="Path to store script's results")
    parser.add_argument("--script-path", type=str, help="Path to algorithm script")
    environment_arguments, script_arguments = arguments_to_dict(*parser.parse_known_args())
    
    algorithm = environment_arguments["algorithm"]
    output_path = environment_arguments["output_path"] \
                if environment_arguments["output_path"] is not None \
                else generate_output_path(algorithm=algorithm) 
    script_path = environment_arguments["script_path"] \
                if environment_arguments["script_path"] is not None \
                else generate_script_path(algorithm=algorithm) 
    target_path = os.path.abspath(os.path.expanduser(environment_arguments["target_path"])) \
                if environment_arguments["target_path"] is not None \
                else None 
                
    output_path = os.path.abspath(os.path.expanduser(output_path))
    script_path = os.path.abspath(os.path.expanduser(script_path)) 
    source_path = os.path.abspath(os.path.expanduser(environment_arguments["source_path"]))
    gt_path = os.path.abspath(os.path.expanduser(environment_arguments["gt_path"]))

    if algorithm not in algorithm_arguments:
        raise NotImplementedError(f"The {algorithm} algorithm is not implemented yet.")
    
    run_script_in_docker(algorithm=algorithm,
                        output_path=output_path,
                        script_path=script_path,
                        source_path=source_path,
                        target_path=target_path,
                        gt_path=gt_path,
                        arguments=script_arguments)
