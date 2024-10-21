# Cisco PKG tool

This tool allows the extraction of .pkg firmware files of Cisco Collaboration Endpoints.

```
usage: cisco_pkg_tool [-h] -f <pkg_filename> [-e <destination_folder>] [-l]

Extract files from Cisco PKG files

options:
  -h, --help            show this help message and exit
  -f, --filename <pkg_filename>
                        PKG file name
  -e, --extract <destination_folder>
                        Extract files to defined folder
  -l, --list            List files in PKG archive
 ```

Example output for Cisco DX80/DX70 firmware file s52040ce9_15_18_5.pkg
 ```
File size: 230493525 bytes
Directory pointer: 0x0143
File count: 31
================================================================================
File ID   Pointer (hex)   File size  File name
================================================================================
      1c             54b        4158  sha512sum.txt
      16            1589      327680  dsp.img
      19           51589     3018752  ducati.img
      17          332589    10231808  /web.img
      29          cf4589          37  partitions.conf.d/web.conf
      1a          cf45ae    11001856  /sounds.img
      29         17725ae       38016  MLO_release_signed_fayette
      27         177ba2e       38016  MLO_release_signed_tempo
      28         1784eae      256744  u-boot_release_signed.bin
      25         17c3996       38016  MLO_dev_signed_fayette
      23         17cce16       38016  MLO_dev_signed_tempo
      24         17d6296      256744  u-boot_dev_signed.bin
      26         1814d7e         164  /partitions.conf.d/main
      19         1814e22          32  /rwfs.conf
      25         1814e42          45  /partitions.conf.d/gui
      17         1814e6f    57352192  /gui.img
      18         4ec6e6f    46878720  /apps.img
      15         7b7be6f     3645080  kernel
      15         7ef5d07    11106259  rootfs
      26         898d4da          48  partitions.conf.d/extra
      18         898d50a    86245376  extra.img
      39         dbcd50a         974  /postinstall.d/00-userfs-migrate.hook.exec
      34         dbcd8d8         894  /postinstall.d/upgrade_fips_mode.exec
      36         dbcdc56        2172  /postinstall.d/upgrade_http_params.exec
      1c         dbce4d2        2531  rwfsfunctions
      2c         dbceeb5        7018  /postinstall.d/rwfs.hook.exec
      26         dbd0a1f           2  /ttparams_schemaversion
      1c         dbd0a21           2  factory.loads
      19         dbd0a23          38  vcinfo.txt
      1a         dbd0a49         264  /target.lst
      22         dbd0b51         516  /pki/signature.pem
 ```