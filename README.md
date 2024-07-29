# eLaw

## The following sections assume the following prerequisites have already been satisfied:
- You have already [set up CumulusCI](https://cumulusci.readthedocs.io/en/latest/tutorial.html) on your device.
- You have already cloned this repository to your device by running: `git clone https://github.com/Nimba-Solutions/eLaw.git`

## Development
   
To work on this project in a scratch org:

1. Run `cci flow run dev_org --org dev --debug` to generate an org and deploy this project.
2. Run `cci org browser dev` to open the org in your browser.


## Releases

To release a new version of this managed package:

1. Run `git checkout main` to switch to the main branch.
2. Run `git pull` to download the latest changes from Github.
3. Run `cci run flow release_2gp_beta --org dev --debug` to release a new 2nd generation managed package.
5. Run `cci org browser dev` to open the org in your browser.
