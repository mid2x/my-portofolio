import boto3
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    porto = s3.Bucket('baalwy.com')
    build = s3.Bucket('codebuild.baalwy.com')

    porto_zip = StringIO.StringIO()
    build.download_fileobj('protofoliobuild.zip', porto_zip)

    with zipfile.ZipFile(porto_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            porto.upload_fileobj(obj, nm, 
            	ExtraArgs={'ContentType' : mimetypes.guess_type(nm)[0]})
            porto.Object(nm).Acl().put(ACL='public-read')
    print "job done!"
    return 'Hello from Lambda'
    