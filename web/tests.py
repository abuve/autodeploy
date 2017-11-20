from django.test import TestCase

# Create your tests here.

import yaml
import json

f = open('docker_test.yaml', 'rb')
data = f.read()
f.close()

yaml_data = yaml.load(data)

print(json.dumps(yaml_data))

f2 = open('docker_new.yaml', 'wb')
#f2.write(yaml.dump(yaml_data).encode())
f2.write(json.dumps(yaml_data).encode())
f2.close()