= Mock Fedora Infrastructure =
This project is a partial mock of some of the critical Fedora infrastructure - namely
Koji (http://koji.fedoraproject.org/koji/) and Bodhi (https://admin.fedoraproject.org/updates/).

Koji is the Fedora build system and is responsible for building RPMs for eventual inclusion
in Fedora. Bodhi is a system for publishing updates and is currently responsible for managing
test feedback and moving builds into and out of repositories that eventually make their way out
to the mirrors.

== Motivation ==
AutoQA is very tightly coupled to both Koji and Bodhi since the tests we run are determined
by what packages have been built and what state they are in (in testing, going to testing,
going to stable etc.).

For general use, this isn't a problem but it does make isolated testing difficult since we
can't do anything without getting build information from Koji and update information from Bodhi.

Since it is difficult to test in isolation, we have ended up doing a decent amount of testing
in production (see http://kparal.wordpress.com/2011/04/29/autoqa-0-4-7-released/). While I do
understand why this is the case, we (the AutoQA developers) don't like it and very much want
to start testing in isolation so that we don't have to put packagers through our bugs that
should have been caught before going into production

== AutoQA Test Structure ==
In order to really understand how Koji and Bodhi fit into AutoQA's dependencies, we need to
understand how AutoQA works with these services and how the data retrieved from them is used.

=== Test Scheduling ===
AutoQA is configured to "watch" certain koji tags corresponding to the currently supported
Fedora releases. Within these releases, we are primarially  interested in the following Koji tags
    * dist-fXX-updates-pending
        - Builds that are currently in updates-testing and will be moved to updates-stable
          at the next repo push by rel-eng
    * dist-fXX-updates-testing-pending
        - Builds that have completed and will be moved to updates-testing at the next repo push

On a regular interval, the AutoQA watcher script pulls data from Koji on changed builds and
schedules checks based on new or changed builds since the last time it ran.

==== Individual Build Tests ====
For builds that are in dist-fXX-updates-testing-pending, the following tests are scheduled:
    - rpmlint
    - rpmguard

==== Batch Build Tests ====
The other major tests that are scheduled by AutoQA involve multiple builds at the same time.
    - depcheck
    - upgradepath

This is an attempt to explain what is going on in AutoQA for tests. I am interested in this
because I want to start mocking out the Fedora infrastructure that we're currently using so
that we can test better without putting stuff into production. I also figure that this could
be useful for other people.

