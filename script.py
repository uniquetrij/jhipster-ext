import os
import re
import fileinput
import shutil
import sys

keywords = ['Auth', 'Audit', 'Mail', 'User', 'Account', 'ClientForward', 'Logout', 'package-info', 'EmailAlreadyUsedException', 'InvalidPasswordException']

try:
    base = sys.argv[1]
except:
    import xml.etree.ElementTree as ET
    base = ET.parse('pom.xml').getroot().find('{*}groupId').text
try:
    ext = sys.argv[2]
except:
    ext = "ext"

base_path = base.replace('.', '/')    
ext_dir = base_path + "/" + ext

root = os.getcwd()
os.chdir("src/main/java/")

try:
    os.remove(ext_dir)
except:
    pass

base_dir_rep = base_path + "/repository"
ext_dir_rep = ext_dir + "/repository"
files = os.listdir(base_dir_rep)
print("----Analyzing repositories...")
idx = 0
for f in files:
    if f.endswith(".java") and not any(keyword in f for keyword in keywords) :
        idx = idx + 1
        print(str(idx) + ". Detected: " + f)
        if not os.path.exists(ext_dir_rep):
            os.makedirs(ext_dir_rep)
        t = open(base_dir_rep + "/" + f, "r")
        contents = t.read()
        t.close()
        contents = contents.replace("package " + base, "package " + base + "." + ext)
        contents = contents.replace("extends", "extends " + base + ".repository." + f.replace(".java", "") + ",")
        contents = re.sub(r'{.*}', "{\n\n}", contents, flags=re.DOTALL)
        t = open(ext_dir_rep + "/" + f, "w")
        t.write(contents)
        t.close()

base_dir_ser = base_path + "/service"
ext_dir_ser = ext_dir + "/service"
files = os.listdir(base_dir_ser)
print("----Analyzing services...")
idx = 0
for f in files:
    if f.endswith(".java") and not any(keyword in f for keyword in keywords) :
        idx = idx + 1
        print(str(idx) + ". Detected: " + f)
        if not os.path.exists(ext_dir_ser):
            os.makedirs(ext_dir_ser)
        t = open(base_dir_ser + "/" + f, "r")
        contents = t.read()
        t.close()
        n = f.replace(".java", "")
        contents = contents.replace("package " + base, "package " + base + "." + ext)
        contents = re.sub(n + ' {.*}', n + r" {\n\n}", contents, flags=re.DOTALL)
        contents = contents.replace(n, n + " extends " + base + ".service." + n)
        t = open(ext_dir_ser + "/" + f, "w")
        t.write(contents)
        t.close()

base_dir_ser_impl = base_path + "/service/impl"
ext_dir_ser_impl = ext_dir + "/service/impl"
files = os.listdir(base_dir_ser_impl)
print("----Analyzing service implementations...")
idx = 0
for f in files:
    if f.endswith(".java") and not any(keyword in f for keyword in keywords) :
        idx = idx + 1
        print(str(idx) + ". Detected: " + f)
        if not os.path.exists(ext_dir_ser_impl):
            os.makedirs(ext_dir_ser_impl)
        t = open(base_dir_ser_impl + "/" + f, "r")
        contents = t.read()
        t.close()
        n = f.replace(".java", "")
        contents = contents.replace("package " + base, "package " + base + "." + ext)
        contents = contents.replace("import " + base + ".service", "import org.springframework.context.annotation.Primary;\nimport " + base + "." + ext + ".service", 1)
        contents = contents.replace("import " + base + ".repository", "import " + base + "." + ext + ".repository", 1)
        contents = contents.replace("implements", "extends " + base + ".service.impl." + n + " implements")
        contents = contents.replace("@Service", '@Primary\n@Service("' + f.replace("Impl.java", "") + '")')
        contents = re.sub(r'}\n.*}', "}\n}", contents, flags=re.DOTALL)
        res = re.search(n + r'\((.*?)\)', contents).group(1)
        s = "super("
        args = res.split(", ")
        for arg in args:
            s = s + arg.split()[1] + ", "
        if len(args) > 0:
            s = s[:-2]
        s = s + ");"
        contents = re.sub(r"(.*)this", r"\g<1>" + s + r"\n\g<1>this", contents, 1)
        t = open(ext_dir_ser_impl + "/" + f, "w")
        t.write(contents)
        t.close()

base_dir_web_rest = base_path + "/web/rest"
ext_dir_web_rest = ext_dir + "/web/rest"
files = os.listdir(base_dir_web_rest)
print("----Analyzing web resources...")
idx = 0
for f in files:
    if f.endswith(".java") and not any(keyword in f for keyword in keywords) :
        idx = idx + 1
        print(str(idx) + ". Detected: " + f)
        if not os.path.exists(ext_dir_web_rest):
            os.makedirs(ext_dir_web_rest)
        t = open(base_dir_web_rest + "/" + f, "r")
        contents = t.read()
        t.close()

        bckup = contents

        n = f.replace(".java", "")
        contents = contents.replace("@RestController", "")
        contents = contents.replace("@RequestMapping(\"/api\")", "@RestController(\"" + n + "\")\n@RequestMapping(\"/api\")")
        contents = contents.replace("package " + base, "package " + base + "." + ext)
        contents = contents.replace("import " + base + ".service", "import " + base + "." + ext + ".service", 1)
        contents = contents.replace("class " + n, "class " + n + " extends " + base + ".web.rest." + n)
        contents = re.sub(r'}\n.*}', "}\n}", contents, flags=re.DOTALL)
        res = re.search(n + r'\((.*?)\)', contents).group(1)
        s = "super("
        args = res.split(", ")
        for arg in args:
            s = s + arg.split()[1] + ", "
        if len(args) > 0:
            s = s[:-2]
        s = s + ");"
        contents = re.sub(r"(.*)this", r"\g<1>" + s + r"\n\g<1>this", contents, 1)
        t = open(ext_dir_web_rest + "/" + f, "w")
        t.write(contents)
        t.close()

        t = open(base_dir_web_rest + "/" + f, "w")
        t.write(bckup.replace("@RestController", ""))
        t.close()


files = os.listdir(base_path)
print("----Analyzing App...")
idx = 0
for f in files:
    if f.endswith("App.java") and not any(keyword in f for keyword in keywords) :
        idx = idx + 1
        print(str(idx) + ". Detected: " + f)
        t = open(base_path + "/" + f, "r")
        contents = t.read()
        t.close()

        bckup = contents

        n = f.replace(".java", "")

        if "EnableJpaRepositories" in contents:
            continue

        contents = contents.replace("import org.springframework.core.env.Environment;","import org.springframework.context.annotation.ComponentScan;\nimport org.springframework.core.env.Environment;\nimport org.springframework.data.jpa.repository.config.EnableJpaRepositories;")
        contents = contents.replace("public class", '@EnableJpaRepositories("' + base + '.' + ext + '")\n@ComponentScan({"' + base + '", "' + base + '.' + ext + '"})' + "\npublic class")

        t = open(base_path + "/" + f, "w")
        t.write(contents)
        t.close()

def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def copy(src, dst):
    l = os.listdir(dst)
    for f in os.listdir(src):
        if os.path.isdir(os.path.join(src, f)):
            copy(os.path.join(src, f), os.path.join(dst, f))
        elif f not in l:
            os.rename(os.path.join(src, f), os.path.join(dst, f))

try:
    os.rename(ext_dir, root + "/" + ext)
except:
    copy(ext_dir, root + "/" + ext)
    remove(ext_dir)
os.symlink(root + "/" + ext, ext_dir)

# print("Please check the generated files and paste the following in your App class")
# print('@EnableJpaRepositories("' + base + '.' + ext + '")\n@ComponentScan({"' + base + '", "' + base + '.' + ext + '"})')
