EEAGlossary

## to be completed ###


EEAGlossary Features

### to be completed ####


EEAGlossary versions

  EEAGlossary version numbers have a three part numeric format separated
  by a dot (x.y.z) where x is the major release number, y is the minor
  release number and z is a maintenance release number.

  o Maintenance releases should be backward compatible, with no changes necessary.

  o Minor releases will require changes to DTML and may require other
  more substantial changes.
  
  o Major releases will require significant changes to any existing EEAGlossary

  The latest release can be downloaded from ### to be completed ###

Support

  If you have any technical problems please contact Antonio De Marinis
  on antonio.de.marinis@eea.eu.int. As this system is new we hope that you
  will send us any comments you might have.

Installation

  Installation of EEAGlossary is the same as for any other Zope product. You
  just need to to untar the package into the Products directory of your
  Zope installation. Consult the Zope documentation if you need further
  information.

  For Windows, you can use Winzip or any similar utility to open the
  EEAGlossary-x-x-x.tar.gz package (where EEAGlossary-x-x-x.tar.gz is the
  name of the EEAGlossary package you downloaded) and extract all the files
  into the appropriate directory.  For Linux and other Unix systems, cd
  to the appropriate directory and do a tar xvzf EEAGlossary-x-x-x.tar.gz
  (where EEAGlossary-x-x-x.tar.gz is the name of the EEAGlossary package
  you downloaded).

  If you are planning to fill the glossary with EEA terms, it is recommended
  that you have the TinyTablePlus Zope product installed. This product
  allows you to store small sets of data in simple and easy to manage
  tables.  The TinyTablePlus product is available at the Zope Products page.

  After installing both the EEAGlossary and TinyTablePlus products, restart
  Zope.  Open the Zope management interface in a web browser (e.g. go to
  http://your-zope-server/manage) and click on the GlossaryEngine if you
  want to change the initial configuration.

  Now select the 'EEA Glossary Centre' option from the pull-down menu
  labeled 'Select type to add...' and create a new centre by entering an
  id,a title and a description.  That's it. Your glossary should now be
  ready to be filled.

  If the 'GlossaryEngine' is not present in the root, then something went
  wrong with the package installation.  Make sure that the EEAGlossary
  package is installed correctly; there should be a EEAGlosary directory
  under the /lib/python/Products directory of your Zope installation. Also,
  make sure that the version of Zope you are using equal or higher than
  2.5.1.

  Another check you can make is to open the Zope management interface and
  click on to the Control Panel folder.  In the control panel folder, click
  on the Product Management link. This will bring up the list of available
  products for your Zope Installation.  If EEAGlosary product is not on the
  list or appears broken, the EEAGlosary package is not installed correctly.
