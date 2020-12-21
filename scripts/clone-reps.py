import os
from git import Repo


def clone_reps(reps, outdir):
    """
    Clone a series of GitHub repositories specified by the "reps" parameter

    :param reps: The list of GitHub repositories to clone
    :param outdir: The directory to clone the repositories on
    """

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for rep in reps:
        repname = rep.split('/')[1]
        repdir = outdir + '/' + repname
        if not os.path.exists(repdir):
            os.makedirs(repdir)

        cloneurl = 'https://github.com/' + rep + '.git'
        print('Cloning ' + cloneurl + '...')
        Repo.clone_from(cloneurl, repdir)


def main():
    clone_reps([
        'Azure/azure-sdk-for-java', 'eclipse/deeplearning4j', 'dropwizard/dropwizard',
        'apache/dubbo', 'ebean-orm/ebean', 'gitblit/gitblit', 'glowroot/glowroot', 'google/guice',
        'JabRef/jabref', 'javamelody/javamelody', 'javaparser/javaparser', 'JodaOrg/joda-time',
        'jhy/jsoup', 'mybatis/mybatis-3', 'scribejava/scribejava', 'apache/spark',
        'jtablesaw/tablesaw', 'code4craft/webmagic'
    ], 'repositories')


if __name__ == '__main__':
    main()
