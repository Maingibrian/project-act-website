import { createReadStream } from 'fs';
import { readFileSync } from 'fs';
import { glob } from 'glob';
import { createInterface } from 'readline';

// Simple deploy using Netlify's deploy API
const NETLIFY_TOKEN = 'nfp_HGHovugyYo1CcLdyg8F9q9ZdFvw5Qz8q0f00';

async function deploy() {
    // First, create a new site
    const siteResp = await fetch('https://api.netlify.com/api/v1/sites', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${NETLIFY_TOKEN}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: 'act-website-kilifi',
            custom_domain: null
        })
    });

    if (!siteResp.ok) {
        const err = await siteResp.text();
        console.error('Site creation failed:', err);
        process.exit(1);
    }

    const site = await siteResp.json();
    console.log('Site created:', site.ssl_url || site.url);

    // Now deploy - upload the directory
    const deployResp = await fetch(`https://api.netlify.com/api/v1/sites/${site.id}/deploys`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${NETLIFY_TOKEN}`,
            'Content-Type': 'application/zip'
        },
        body: readFileSync('website-deploy.tar')
    });

    if (!deployResp.ok) {
        const err = await deployResp.text();
        console.error('Deploy failed:', err);
        process.exit(1);
    }

    const deploy = await deployResp.json();
    console.log('Deployed!');
    console.log('Site URL:', deploy.ssl_url || deploy.url);
    console.log('Deploy URL:', deploy.deploy_url || deploy.ssl_url);
}

deploy().catch(console.error);