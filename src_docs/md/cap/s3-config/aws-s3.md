# AWS S3

*Use an Amazon S3 bucket for new Vexy Screensese uploads*

Vexy Screensese can use a private Amazon S3 bucket for new shareable-link uploads. Existing recordings remain on their current storage provider.

## Create the bucket and credentials

Create a private S3 bucket in the region you plan to enter in Vexy Screensese. Keep public access blocked; Vexy Screensese reads objects through its storage layer and normal access checks.

Create a dedicated IAM identity with access only to that bucket. Vexy Screensese currently needs to test the bucket, read and write objects, delete objects, and complete or abort multipart uploads. A starting policy is:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::BUCKET_NAME"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": ["arn:aws:s3:::BUCKET_NAME/*"]
    }
  ]
}
```

Replace `BUCKET_NAME` before saving. Apply narrower prefixes if your organization has an established storage policy.

## Configure CORS

Browser uploads use presigned requests and need the `ETag` response header. Add every web origin that will upload through Vexy Screensese, including your custom or self-hosted domain if applicable:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "HEAD", "PUT"],
    "AllowedOrigins": ["https://cap.so"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3000
  }
]
```

Do not copy origins you do not use. Add the exact scheme and host for each trusted Vexy Screensese deployment.

## Connect Vexy Screensese

1. Open **Settings > Integrations > S3 Config**.
2. Select **AWS S3**.
3. Enter the dedicated access-key ID and secret access key.
4. Enter `https://s3.amazonaws.com` or the endpoint required by your AWS setup.
5. Enter the bucket name and region.
6. Click **Test Connection**.
7. Save only after the test succeeds.

The connection test performs a bucket-head request. A successful test confirms the credentials can reach the bucket, but a sample upload and playback is still required to verify object and CORS permissions.

## Organization-managed storage

Owners and admins can manage S3 at the organization level. When organization storage is active, members see that the integration is managed by the organization and cannot replace the configuration in Vexy Screensese.

Changing the active provider affects future uploads. It does not bulk-move existing Vexy Screensese, Google Drive, or S3 objects.

## Verify before rollout

1. Upload one non-sensitive sample recording.
2. Confirm the object appears in the intended bucket and prefix.
3. Open the recording link as an allowed viewer.
4. Confirm playback and any download behavior you intend to support.
5. Delete the sample recording and confirm your retention expectations.

Store credentials in Vexy Screensese's configuration flow, not in chat, tickets, or source control.
