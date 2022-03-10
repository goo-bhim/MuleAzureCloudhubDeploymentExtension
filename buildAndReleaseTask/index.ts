import tl = require('azure-pipelines-task-lib/task');
import path = require('path');
import { TaskMockRunner } from 'azure-pipelines-task-lib/mock-run';

tl.setResourcePath(path.join(__dirname, 'task.json'));
const task_dir = __dirname;

async function run() {
    try {
        process.env.artifact_drop_path = tl.getInput('artifactDropPath', true);
        process.env.cloudhub_user = tl.getInput('cloudhubUser', true);
        process.env.cloudhub_pass = tl.getInput('cloudhubPass', true);
        process.env.org_id = tl.getInput('organizationId', true);
        process.env.env_id = tl.getInput('environmentId', true);
        process.env.domain_name = tl.getInput('domainName', true);
        process.env.mule_version = tl.getInput('muleVersion', true);
        process.env.region = tl.getInput('region', true);
        process.env.monitoring_enabled = tl.getBoolInput('monitoringEnabled', true) ? "True" : "False";
        process.env.monitoring_auto_restart = tl.getBoolInput('monitoringAutoRestart', true) ? "True" : "False";
        process.env.workers_amount = tl.getInput('workerAmount', true);
        process.env.workers_type_name = tl.getInput('workerTypeName', true);
        process.env.anypoint_platform_client_id = tl.getInput('anypointPlatformClientId', false);
        process.env.anypoint_platform_client_secret = tl.getInput('anypointPlatformClientSecret', false);
        process.env.cloudhub_environment = tl.getInput('cloudhubEnvironment', false);
        process.env.security_key = tl.getInput('securityKey', false);
        process.env.logging_enabled = tl.getBoolInput('loggingEnabled', true) ? "True" : "False";
        process.env.persistent_queues = tl.getBoolInput('persistentQueues', true) ? "True" : "False";
        process.env.object_store_v1 = tl.getBoolInput('useObjectStoreV2', true) ? "False" : "True";

        process.env.additional_properties = tl.getInput('additionalProperties', true);
        const additional_properties = process.env.additional_properties || '{}';

        const python = tl.tool(tl.which('python3')).arg([task_dir + "/cloudhub_deployment.py", additional_properties]);

        await python.exec(<any>{
            cwd: ".",
            failOnStdErr: true,
            errStream: process.stdout,
            outStream: process.stdout,
            ignoreReturnCode: false
        });
    }
    catch (err) {
        tl.setResult(tl.TaskResult.Failed, err.message);
    }
}

run();