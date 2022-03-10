**Introduction**
The Cloudhub Deployment Pipeline task Extension is specifically build for Azure Pipelines. The pipeline task extension could be used to locates a Mule 4 build artifact, and deploys it to a specific Anypoint Cloudhub business organization and environment (with configuration) specified by the pipeline running the extension. This source code could be used for reference purpose and can be customize as per individual organization need.

Azure Devops tasks extensions are build using JSON, HTMS, JS, TS, CSS and Python. You can build the extensions in the language of your choice. The main script uses Anypoint Cloudhub rest api for the deployment.
**Anypoint Cloudhub REST API https://anypoint.mulesoft.com/exchange/portals/anypoint-platform/f1e97bc6-315a-4490-82a7-23abe036327a.anypoint-platform/cloudhub-api/**


**Notes**
Please update following files

task.json: id, name, friendlyName, description and author.

package.json: version number.


**Detailed Steps to create task extensions**
Please refer below document on how to create custom task extensions
https://docs.microsoft.com/en-us/azure/devops/extend/develop/add-build-task?view=azure-devops
