import boto3
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic("arn:aws:sns:us-east-1:980307711485:snsPublishDeploy")
    location = {
        "bucketName":'codebuild.baalwy.com',
        "objectKey":'protofoliobuild.zip'
    }
    try:
        job = event.get("CodePipeline.job")
        
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"]=="MyAppBuild":
                    location = artifact["location"]["s3Location"]
        print "Building portofolio from " + str(location)           
        s3 = boto3.resource('s3')
        porto = s3.Bucket('baalwy.com')
        build = s3.Bucket(location["bucketName"])
    
        porto_zip = StringIO.StringIO()
        build.download_fileobj(location['objectKey'], porto_zip)
    
        with zipfile.ZipFile(porto_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                porto.upload_fileobj(obj, nm, 
                    ExtraArgs={'ContentType' : mimetypes.guess_type(nm)[0]})
                porto.Object(nm).Acl().put(ACL='public-read')
        
        topic.publish(Subject = "Portofolio Deployed", Message= "This is from Try Block")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject = "Portofolio Deployed Failed", Message= "This is from exception Block")
        raise

    return 'Hello from Lambda'
    