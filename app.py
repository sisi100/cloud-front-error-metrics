import aws_cdk as cdk
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_s3 as s3

app = cdk.App()
stack = cdk.Stack(app, "cloud-front-error-metrics-stack")

# バケットを作成する
bucket = s3.Bucket(
    stack,
    "DummyBucket",
    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
    removal_policy=cdk.RemovalPolicy.DESTROY,
    auto_delete_objects=True,
)
log_bucket = s3.Bucket(
    stack,
    "LogBucket",
    access_control=s3.BucketAccessControl.LOG_DELIVERY_WRITE,
    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
    removal_policy=cdk.RemovalPolicy.DESTROY,
    auto_delete_objects=True,
)

cf_function = cloudfront.Function(stack, "Function", code=cloudfront.FunctionCode.from_file(file_path="function.js"))

# CloudFrontのディストリビューションを作成する
distribution = cloudfront.Distribution(
    stack,
    "Distribution",
    default_behavior=cloudfront.BehaviorOptions(
        origin=origins.S3Origin(bucket),
        function_associations=[
            cloudfront.FunctionAssociation(
                function=cf_function, event_type=cloudfront.FunctionEventType.VIEWER_REQUEST
            ),
        ],
    ),
    default_root_object="index.html",
    log_bucket=log_bucket,
    log_file_prefix="cloudfront",  # DatadogのログをCloudFrontのログとして扱うために、ログのプレフィックスを指定する
)

app.synth()
