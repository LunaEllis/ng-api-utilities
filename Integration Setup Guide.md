# API Integrations: A Quick Setup Guide
_Note that if you aren't releasing a project available to the public, this is probably unneccessary._

# 1. Why bother?
The default rate limit is 250 requests per hour. By setting up an integration, the rate limit is increased to 1000 requests per hour.
This doesn't matter for people making small projects that aren't going to be used by very many people. However, if you're developing projects such as a
stats tracker that many people are likely to use, then it's highly recommended to set up an integration, as it reduces the likelihood of too many people
using your project once and reaching the rate limit.

_A 'rate limit' is the maximum number of requests the NG API will accept over the span of 1 hour._

# 2. What is an 'API integration' anyway?
An API integration is simply an app that you tell NG about. In exchange, it creates an authorization key that you send along with requests. This key
tells the API that it's an authorized request, allowing all requests using the key to use the increased rate limit.

# 3. How do I set up an integration?
It's a very straightforward process:

Step 1: Login to the NG portal, found at https://portal.nethergames.org/auth/account
![login](https://user-images.githubusercontent.com/69582383/130303102-d3357307-7c49-4528-9ea1-33d398241a55.PNG)

Step 2: Click on the button that says 'Manage API Integrations'
![click manage api integrations](https://user-images.githubusercontent.com/69582383/130303123-1d89180a-d474-4b30-9baf-8f517935c6a0.PNG)

Step 3: Click on the button that says 'Create API Integration'
![click create api integration](https://user-images.githubusercontent.com/69582383/130303132-3e3dcd85-2f45-431b-9d9080f4ca1f6786.PNG)

Step 4: Fill out the name and description of the integration
![fill out name and description](https://user-images.githubusercontent.com/69582383/130303174-d2bbce3a-c194-4461-aa27-33b9600e4e71.PNG)

Step 5: Click on your new integration
![click on your new integration](https://user-images.githubusercontent.com/69582383/130303191-055b9601-cd8f-469f-ac98-5d59ae70222a.PNG)

Step 6: Click the 'Copy' button to copy the authorization key to your clipboard
![click copy](https://user-images.githubusercontent.com/69582383/130303211-6a4a3793-c945-4001-a3c0-96df249b6ca8.PNG)

Step 7: Create a file named 'auth_key.txt' in the same folder as the 'api_utilities.py' file
![create a text file named auth key](https://user-images.githubusercontent.com/69582383/130303246-adca9c3f-fdd1-4963-8059-4133e5def0d6.PNG)

Step 8: Paste the auth key into the text file, and save it
![paste code into text file](https://user-images.githubusercontent.com/69582383/130303272-c4e4ca71-7801-465b-ad3a-1ae48d3cdd01.PNG)

And voila! You've now integrated your app!
