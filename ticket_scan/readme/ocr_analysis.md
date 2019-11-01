# OCR Analysis

Summary of results with OCR. As of 3 Oct 2019 two tests were done to check how did payed services of OCR performed as
compared to the algorithms we implemented here.

In a first approach Microsoft's service was not as convincing as Amazon's so a couple of details will be given on this last one only.

- A test service is available (no account needed) where an image can be tested [here](https://us-east-2.console.aws.amazon.com/textract/home?region=us-east-2#/demo)
- Pricing can be checked out [here](https://aws.amazon.com/textract/pricing/). Main advantages: pay for use, OCR service is the cheapest in Computer Vision (~1.50$ for 1000 pages - EU Ireland server prices). 
- An account can be created following [this](https://docs.aws.amazon.com/textract/latest/dg/getting-started.html) start guide. Although there is already an administrator account created that can give access and create other accounts to test (Miguel).
- A bucket must be created for the service to work with images that are **already** uploaded into the bucket.
  - On a production environment, the aws-cli or boto3 (the tools provided by AWS) would have to be used to do the upload. In any case architecture would be a change, **the previous point refers to tests and notebook in proyect**.

At first AWS detects correctly most of the ticket (even more than we do as of now, for the example used). Following, an example of one of the texts detected and returned in the response:
```
[ 
  # ...
  {'BlockType': 'LINE',
  'Confidence': 71.305419921875,
  'Text': 'MERCADONA S S.A. A -O',
  'Geometry': {'BoundingBox': {'Width': 0.5924637317657471,
    'Height': 0.014716140925884247,
    'Left': 0.2752343714237213,
    'Top': 0.06579777598381042},
   'Polygon': [{'X': 0.2752343714237213, 'Y': 0.06579777598381042},
    {'X': 0.867698073387146, 'Y': 0.06579777598381042},
    {'X': 0.867698073387146, 'Y': 0.08051391690969467},
    {'X': 0.2752343714237213, 'Y': 0.08051391690969467}]},
  'Id': '640273c1-e92c-4b79-89ba-2e20bef5f174',
  'Relationships': [{'Type': 'CHILD',
    'Ids': ['01caab35-eb44-4fda-a1fd-0de39f1f1575',
     'cd4edff5-ad6c-4a0b-b625-f3d53e5df3c9',
     '0a542472-ee4e-48f0-b55b-ba65a42b01b1',
     '48795198-fcf5-4f5f-b31e-61a2b34388f9',
     '714372f2-aff2-42bf-8167-8fb9734dc217']}]},
 {'BlockType': 'LINE',
  'Confidence': 89.66963195800781,
  'Text': 'C/ MAYOR, 7 ESPINARDO',
  'Geometry': {'BoundingBox': {'Width': 0.4979221224784851,
    'Height': 0.01784255914390087,
    'Left': 0.25247466564178467,
    'Top': 0.11675985157489777},
   'Polygon': [{'X': 0.25247466564178467, 'Y': 0.11675985157489777},
    {'X': 0.7503967881202698, 'Y': 0.11675985157489777},
    {'X': 0.7503967881202698, 'Y': 0.1346024125814438},
    {'X': 0.25247466564178467, 'Y': 0.1346024125814438}]},
  'Id': '96f3aa64-0316-4213-9472-1413e5afe947',
  'Relationships': [{'Type': 'CHILD',
    'Ids': ['44fd17c9-b84f-4545-99b7-339bea76840e',
     '68b0843b-97f1-4efc-a1a0-8b184538ac71',
     'ec881e63-9234-4e98-84d4-c9a08c806beb',
     '8c0d83eb-a0a9-4b76-aa47-7fe8fdf92d16']}]}
     #...
]
```
