import os
import re
import fileinput

keywords = ['Auth', 'Audit', 'Mail', 'User', 'Account', 'ClientForward', 'Logout', 'package-info']

base = input("Enter base package name: ")
base_path = base.replace('.', '/')
ext = input("Enter ext folder name: ")
ext_dir = base_path + "/" + ext

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
        contents = contents.replace("import " + base + ".service", "package " + base + "." + ext + ".service", 1)
        contents = contents.replace("import " + base + ".repository", "package " + base + "." + ext + ".repository", 1)
        contents = contents.replace("extends", "extends " + base + ".service.impl." + n)
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
        contents = contents.replace("package " + base, "package " + base + "." + ext)
        contents = contents.replace("import " + base + ".service", "import " + base + "." + ext + ".service", 1)
        contents = contents.replace("extends", "extends " + base + ".web.rest." + n)
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

print("Please check the generated files and paste the following in your App class")
print('@EnableJpaRepositories("' + base + '.' + ext + '")\n@ComponentScan({"' + base + '", "' + base + '.' + ext + '"})')
