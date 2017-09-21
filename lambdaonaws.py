import boto3
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic("arn:aws:sns:us-east-1:980307711485:snsPublishDeploy")
    try:
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
        
        topic.publish(Subject = "Portofolio Deployed", Message= "This is from Try Block")
    except:
        topic.publish(Subject = "Portofolio Deployed Failed", Message= "This is from exception Block")
        raise

    return 'Hello from Lambda'
    
    