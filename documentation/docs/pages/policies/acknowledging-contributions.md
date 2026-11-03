## Scope
How we will recognise and manage software contributions at ACCESS-NRI.

## Purpose and Background
At ACCESS-NRI we strive to be a collaborative, multidisciplinary and equitable organisation with diverse and inclusive culture (see [values](https://www.access-nri.org.au/about/aims/)). Collaboration is at the core of our work and is paramount to the quality of our work. This policy document sets out transparent and best-practice guidelines for how we expect technical code work to be acknowledged both within our organisation and in working with our external partners. 

Why is it useful for contributions to be acknowledged? Specifically, for the author of the code to be the author of the commit?
 - Useful for career growth as contributions are aligned with GitHub metrics;
 - Future users/developers know who to contact about the code;
 - Related publications/outputs can involve appropriate authors.

## Who’s responsibility is this?
It is up to all of us to build a culture of good practice. Practically, the lead role can vary but for ACCESS-NRI code repositories, the project lead/lead developer/first author takes on the role of ensuring we follow these guidelines wherever possible. For the rest of this document, this person is called ‘project lead’. This can’t apply for repositories we don't host or look after directly. When issues arise, the issue should be raised in the first instance to the lead as described (see below for further guidance).

## Who is a contributor? 
 - those who commit code to the software. These commits may be to software source code itself or to things that support the software (e.g. documentation, tests and infrastructure that supports the software, such as CI/CD, build systems etc);
 - those who provide other useful contribution     to the software, for example through design scoping, testing, code reviews and deployment.

Additionally, see [ANU’s policy](https://policies.anu.edu.au/ppl/document/ANUP_6747116#:~:text=An%20author%20is%20responsible%20not,be%20accountable%20for%20its%20integrity.).

## How do we recognise a contribution?
 - If the code is managed on GitHub, then the author of the code changes should be an author of the Git commit (full name used);
 - Coauthor on related publication  s/release DOIs;
 - Specific mention of contribution in acknowledgements text (e.g. journal publications, GitHub README.md etc)

The suggested workflow for when:
1.	Employees go on leave;
a.	Employee should communicate with colleagues what their preference is if situations arise where colleagues need to commit their code.
b.	Use [co-author commits](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors).
2.	We receive code changes from the community that they would like us to commit on their behalf;
a.	Have a conversation with the code author about their preference. If they have a GitHub account, then you could help them commit the code themselves. Similarly, perhaps they would like to set up a GitHub account so their contribution can be acknowledged 
b.	If possible, use [co-author commits](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors). If not possible (e.g. no GitHub account), cite their name with contact information.
3.	Using an exact Git commit from another upstream organisation, cherry pick the commit such that the original author becomes the lead author and the pickee becomes the ‘committed’ coauthor (GitHub’s default behaviour).

## Code of practice through examples
If something unfortunate happens, you are first encouraged to talk to the project lead, and then your line manager. After those avenues, you can also talk to the [Executive team](https://www.access-nri.org.au/teams/executive-team/) and we can put together an ethics committee to provide guidance. This can be confidential.
Below are some fictional examples that demonstrate how the above workflow can be applied:
1.	[POSITIVE] When a new contributor Abraham makes a contribution to a GitHub repository, Abraham speaks to the repository admin about being acknowledged as a contributor in the Zenodo archive. (In some instances, this can be done through adding their name to the end of the `.zenodo.json` file.) Abraham thus has a citable reference for which they can demonstrate they contributed to the repository.
2.	[NEGATIVE] Anahera is working on their PhD project using the existing ACCESS-NRI regional modelling framework.  Anahera improves the framework such that new tracer boundary conditions are supported, and their supervisor commits it to the repository. Anahera is frustrated as not getting credited for work will make it harder to get their dream post-PhD software engineering job. Anahera’s supervisor is now being asked lots of questions about the code which the supervisor can’t answer as they were not involved in the development.
3.	[QUESTION] As part of her postdoc work, Bindi has created a script to analyse model output. Whilst she wrote the code herself, she did have guidance from a fellow postdoc on how best to approach the analysis. Bindi now wants to submit this code to a GitHub repository but is unsure as to whether her fellow postdoc needs credited for their help. In this situation, it is important for Bindi to chat with her fellow postdoc as early as possible in the process so that they can set expectations. Not being involved in writing the code does not exclude the fellow postdoc if they have made other intellectual input and the two of them should try to come to an agreement on whether the input was significant enough to warrant credit (co-authorship of a commit is a possibility for instance). If in doubt, they can reach out to people such as their supervisor or the GitHub repository maintainers to seek further advice.   
4.	[POSITIVE]: James works at ACCESS-NRI and is developing the coupled model “Cloudy#5”; James asks for specific help on how to take the next technical steps to release Cloudy#5. Sharon  in the release team, helps James with some infrastructure coding that builds the model ready for community release. James finds Sharon’s input super valuable. With Sharon’s permission, she is included on: the GitHub release contributor list and they are acknowledged in the subsequent technical report.
5.	[QUESTION] Janice is working on a stand-alone piece of ACCESS-NRI software which has completed a development cycle and is ready for community Alpha release.  In order to do this, an existing ACCESS-NRI deployment workflow/toolbox/pipeline is utilised (e.g. Spack, Github actions etc.). As these tools form a key part of the deployment process, the authors of the ACCESS-NRI deployment tools/code could be listed as contributors but on discussion the release team feel that major changes were not required and do not feel like they need to be individually acknowledged as authors. The subsequent, community written, description paper does mention (acknowledgements) the support of the ACCESS-NRI release infrastructure as being invaluable for supporting the work.
Note: ACCESS-NRI will remedy incorrect zenodo author lists when notified. We encourage project leads (see responsibility heading above) to be as inclusive as possible.

We welcome feedback on these guidelines and please feel free to contribute or discuss with your line managers.

**Written March 2025**: Christopher Bull. Feedback: Kelsey Druken, Dougie Squire, Clare Richards, Michael Tetley, Paul Leopardi, Helen Macdonald, Aidan Heerdegen.

Further reading
 - [ANU authorship guidance](https://policies.anu.edu.au/ppl/document/ANUP_6747116)
 - [ANU Form: Responsible conduct of research authorship Document](https://policies.anu.edu.au/ppl/document/ANUP_000964) 
 - [Australian Code for the Responsible Conduct of Research, 2018](https://www.nhmrc.gov.au/about-us/publications/australian-code-responsible-conduct-research-2018)