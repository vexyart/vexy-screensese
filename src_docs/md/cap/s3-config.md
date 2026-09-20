# S3-compatible Storage

*Connect private object storage for new Vexy Screensese uploads*

Vexy Screensese can store new shareable-link uploads in your own S3-compatible bucket. Vexy Screensese currently offers presets for AWS S3, Cloudflare R2, Supabase, MinIO, and other S3-compatible providers.

## How it works

- The active configuration applies to new uploads.
- Existing recordings stay on their current storage provider.
- Viewers still use Vexy Screensese share and embed routes, with normal access checks.
- Personal storage can be configured in Vexy Screensese.
- Organization owners and admins can manage storage centrally for members.

Changing or removing a configuration does not automatically copy existing objects to another provider.

## Configure a provider

1. Create a private bucket and dedicated credentials with the object and multipart permissions Vexy Screensese needs.
2. Configure browser CORS for every trusted Vexy Screensese web origin and expose the `ETag` response header.
3. Open **Vexy Screensese > Settings > Integrations > S3 Config**.
4. Choose the provider and enter the access-key ID, secret access key, endpoint, bucket name, and region.
5. Click **Test Connection**, then save.
6. Upload and play a non-sensitive sample before using the bucket for the team.

Use the provider-specific instructions:

- [AWS S3](s3-config/aws-s3.md)
- [Cloudflare R2](s3-config/cloudflare-r2.md)

See the Google Drive storage option instead of S3-compatible storage.

## Security boundary

Keep the bucket private and scope credentials to the intended bucket or prefix. Enter secrets through Vexy Screensese's protected configuration surface, not through chat or source control. A successful connection test proves bucket access; the sample upload verifies object permissions, multipart CORS, storage, and playback together.
