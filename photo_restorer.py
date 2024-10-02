from dotenv import load_dotenv
load_dotenv()
import replicate
import os
my_secret = os.environ['REPLICATE_API_TOKEN']


'''


output = replicate.run(
  "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
  input={
    "img": "https://replicate.delivery/pbxt/JuWqd7JcJm55zYHnjDDs0w0fmZTPMh1CKKHeqNPVMjdMVVRq/IMG_20230806_180541_779.jpg",
    "scale": 2,
    "version": "v1.4"
  }
)
print(output)



**********
model = replicate.models.get("tencentarc/gfpgan")
version = model.versions.get("9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3")


def predict_image(filename):
  input={
    "img": open(filename, "rb"),
    "scale": 2,
    "version": "v1.4"
  }
  output = version.predict(**input)
  #output = model.predict(**input)
  print(output)
  return output
'''



def predict_image(filename):
  output = replicate.run(
  "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
  input={
    "img": open(filename, "rb"),
    "scale": 2,
    "version": "v1.3"
  }
)
  print(output)
  return output

  




