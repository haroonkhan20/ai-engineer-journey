from roboflow import Roboflow
rf = Roboflow(api_key="")
project = rf.workspace("haroons-workspace-ani0d").project("water-bottle-phone-detector")
version = project.version(2)
dataset = version.download("yolov8")
                              
print(f"Dataset downloaded to: {dataset.location}")
                