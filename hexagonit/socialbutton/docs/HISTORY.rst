Change log
----------

0.8.1 (2012-09-28)
==================

- Fixed bug for multiple line code. [rnd, taito]

0.8 (2012-09-20)
================

- Added dependency to Plone>=4.2.1 and removed dependency to plone.stringinterp>=1.0.7 since Plone-4.2.1 includes it.
  [taito]

0.7 (2012-08-22)
================

- Dependency to plone.stringinterp>=1.0.7 added to make string interpolation available
  in the context of Plone Site root.
  [taito]

0.6 (2012-08-21)
================

- Added guards for cases of None to the upgrade step [rnd]

0.5 (2012-08-17)
================

- Updated registry.xml to enable import and export. [taito]
- Switched to use plone.stringinterp instead of format method
  for string interpolation in embedding codes.
  [taito]

0.4 (2012-08-13)
================

- Fixing typo. Po-files initialized. Some translations. [rnd]
- Fixing the problem with some views: guarding the viewlet [rnd]
- google-plus image added [taito]

0.3 (2012-08-08)
================

- Added class for styling against viewlet managers. [rnd]

0.2 (2012-08-02)
================

- Uninstall profile to remove registry records added. [taito]
- UnicodeDecodeError for context title and description fixed for the viewlet. [taito]
- Added 'Plone Site' to the configurable content types. [taito]

0.1 (2012-07-31)
================

- Initial release for use. [taito]

0.0 (2012-07-24)
================

- Initial release. [taito]
