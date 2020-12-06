import glob
import inspect
import os
import pprint
from importlib import import_module

import settings
from skill_class import AssistantSkill

skills_path = "../skills"
skills_directory = os.path.join(settings.BASE_DIR, skills_path)

skills_directories = [dir for dir in glob.glob(os.path.join(skills_directory, "*")) if os.path.isdir(dir)]

for skill_path in skills_directories:
    skill_module_name = os.path.join(skill_path, "skills.py")
    if os.path.exists(skill_module_name):
        skill_module_path = "{}.skills".format(
            skill_path.replace(str(settings.BASE_DIR), "").replace(os.path.sep, ".")
        )[1::]
        skill_module = import_module(skill_module_path)

        for skill_class_name in dir(skill_module):
            if skill_class_name != "AssistantSkill":
                skill_class = getattr(skill_module, skill_class_name)

                if inspect.isclass(skill_class) and issubclass(skill_class, AssistantSkill):
                    settings.SKILLS_REGISTRY.append(skill_class)
