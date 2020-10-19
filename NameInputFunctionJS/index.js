const cosmos = require('@azure/cosmos');
const { CosmosClient } = cosmos;

const client = new CosmosClient('AccountEndpoint=https://tst-azure.documents.azure.com:443/;AccountKey=89lhKSndZ8tsZx4X9g8xrKez2IbMH0lJliJEdNnP1PdXSAGin42M952uBkCUbyFX1HmhDUt71gKYZSaygEL3tA==;');
const container = client.database('demodb').container('items');

module.exports = async function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const name = (req.query.name || (req.body && req.body.name));
    const responseMessage = name
        ? "Hello, " + name + ". This HTTP triggered function executed successfully."
        : "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.";
    
    const newItem = { name : name, time: Date() };
    const { resource: createdItem } = await container.items.create(newItem);
    
    context.res = {
        // status: 200, /* Defaults to 200 */
        body: responseMessage
    };
}