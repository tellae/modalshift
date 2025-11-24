# MODALSHIFT

Open developments for MODALSHIFT EU project

## Configuration file

Put a file name config.yml at root.

Here is an example configuration.

```yaml
S3_server: https://url
S3_id_env_name: S3_ID
S3_secret_env_name: S3_SECRET
output_directory: data/ 
```

## Download a file

```python
python3 src/get_data_from_S3.py
```
