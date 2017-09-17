import boto3
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3')
porto = s3.Bucket('baalwy.com')
#for obj in porto.objects.all():
 #   print obj.key
#porto.download_file('index.html','/tmp/index.html')
build = s3.Bucket('codebuild.baalwy.com')
#build.download_file('portofoliobuild.zip', '/tmp/portofoliobuild.zip')
#for obj in porto:
#    print obj.key
#for obj in build.objects.all()
#for obj in build.objects.all():
#    print obj.key
#build.download_file('protofoliobuild.zip', '/tmp/portofoliobuild.zip')
#build.download_file('protofoliobuild.zip', porto_zip)

porto_zip = StringIO.StringIO()
build.download_fileobj('protofoliobuild.zip', porto_zip)

with zipfile.ZipFile(porto_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        porto.upload_fileobj(obj, nm, 
        	ExtraArgs={'ContentType' : mimetypes.guess_type(nm)[0]})
        porto.Object(nm).Acl().put(ACL='public-read')
