#
# Generated waf script.
#

try:
    import rtems_waf.rtems as rtems
except:
    print "error: no rtems_waf git submodule; see README.waf"
    import sys
    sys.exit(1)

def init(ctx):
    rtems.init(ctx)

def options(opt):
    rtems.options(opt)

def configure(conf):
    conf.find_program("lex", mandatory = True)
    conf.find_program("rpcgen", mandatory = True)
    conf.find_program("yacc", mandatory = True)
    rtems.configure(conf)
    if rtems.check_networking(conf):
        conf.fatal("RTEMS kernel contains the old network support; configure RTEMS with --disable-networking")

def build(bld):
    rtems.build(bld)

    # C/C++ flags
    common_flags = []
    common_flags += ["-O"]
    common_flags += ["-g"]
    common_flags += ["-fno-strict-aliasing"]
    common_flags += ["-ffreestanding"]
    common_flags += ["-fno-common"]
    common_flags += ["-Wno-implicit-function-declaration"]
    cflags = ['-std=gnu11'] + common_flags
    cxxflags = ['-std=gnu++11'] + common_flags

    # Include paths
    includes = []
    includes += ["rtemsbsd/include"]
    includes += ["freebsd/sys"]
    includes += ["freebsd/sys/contrib/altq"]
    includes += ["freebsd/sys/contrib/pf"]
    includes += ["freebsd/include"]
    includes += ["freebsd/lib/libc/include"]
    includes += ["freebsd/lib/libc/isc/include"]
    includes += ["freebsd/lib/libc/resolv"]
    includes += ["freebsd/lib/libutil"]
    includes += ["freebsd/lib/libkvm"]
    includes += ["freebsd/lib/libmemstat"]
    includes += ["freebsd/lib/libipsec"]
    includes += ["rtemsbsd/sys"]
    includes += ["mDNSResponder/mDNSCore"]
    includes += ["mDNSResponder/mDNSShared"]
    includes += ["mDNSResponder/mDNSPosix"]
    includes += ["testsuite/include"]
    for i in ['-Irtemsbsd/@CPU@/include', '-Ifreebsd/sys/@CPU@/include']:
        includes += ["%s" % (i[2:].replace("@CPU@", bld.get_env()["RTEMS_ARCH"]))]

    # Support dummy PIC IRQ includes
    if bld.get_env()["RTEMS_ARCH"] not in ("arm", "i386", "lm32", "mips", "powerpc", "sparc", "m68k"):
        includes += ["rtems-dummy-pic-irq/include"]

    # Collect the libbsd uses
    libbsd_use = []

    # KVM Symbols
    bld(target = "rtemsbsd/rtems/rtems-kvm-symbols.c",
        source = "rtemsbsd/rtems/generate_kvm_symbols",
        rule = "./${SRC} > ${TGT}")
    bld.objects(target = "kvmsymbols",
                features = "c",
                cflags = cflags,
                includes = includes,
                source = "rtemsbsd/rtems/rtems-kvm-symbols.c")
    libbsd_use += ["kvmsymbols"]

    # RPC Generation
    bld(target = "freebsd/include/rpc/rpcb_prot.h",
        source = "freebsd/include/rpc/rpcb_prot.x",
        rule = "${RPCGEN} -h -o ${TGT} ${SRC}")

    # Route keywords
    rkw_rule = "cat ${SRC} | awk 'BEGIN { r = 0 } { if (NF == 1) printf \"#define\\tK_%%s\\t%%d\\n\\t{\\\"%%s\\\", K_%%s},\\n\", toupper($1), ++r, $1, toupper($1)}' > ${TGT}"
    bld(target = "freebsd/sbin/route/keywords.h",
        source = "freebsd/sbin/route/keywords",
        rule = rkw_rule)

    # Lex
    bld(target = "freebsd/lib/libc/net/nslexer.c",
        source = "freebsd/lib/libc/net/nslexer.l",
        rule = "${LEX} -P _nsyy -t ${SRC} | sed -e '/YY_BUF_SIZE/s/16384/1024/' > ${TGT}")
    bld.objects(target = "lex__nsyy",
                features = "c",
                cflags = cflags,
                includes = includes,
                source = "freebsd/lib/libc/net/nslexer.c")
    libbsd_use += ["lex__nsyy"]

    bld(target = "freebsd/lib/libipsec/policy_token.c",
        source = "freebsd/lib/libipsec/policy_token.l",
        rule = "${LEX} -P __libipsecyy -t ${SRC} | sed -e '/YY_BUF_SIZE/s/16384/1024/' > ${TGT}")
    bld.objects(target = "lex___libipsecyy",
                features = "c",
                cflags = cflags,
                includes = includes,
                source = "freebsd/lib/libipsec/policy_token.c")
    libbsd_use += ["lex___libipsecyy"]

    # Yacc
    bld(target = "freebsd/lib/libipsec/policy_parse.c",
        source = "freebsd/lib/libipsec/policy_parse.y",
        rule = "${YACC} -b __libipsecyy -d -p __libipsecyy ${SRC} && sed -e '/YY_BUF_SIZE/s/16384/1024/' < __libipsecyy.tab.c > ${TGT} && rm -f __libipsecyy.tab.c && mv __libipsecyy.tab.h freebsd/lib/libipsec/y.tab.h")
    bld.objects(target = "yacc___libipsecyy",
                features = "c",
                cflags = cflags,
                includes = includes,
                source = "freebsd/lib/libipsec/policy_parse.c")
    libbsd_use += ["yacc___libipsecyy"]
    bld(target = "freebsd/lib/libc/net/nsparser.c",
        source = "freebsd/lib/libc/net/nsparser.y",
        rule = "${YACC} -b _nsyy -d -p _nsyy ${SRC} && sed -e '/YY_BUF_SIZE/s/16384/1024/' < _nsyy.tab.c > ${TGT} && rm -f _nsyy.tab.c && mv _nsyy.tab.h freebsd/lib/libc/net/nsparser.h")
    bld.objects(target = "yacc__nsyy",
                features = "c",
                cflags = cflags,
                includes = includes,
                source = "freebsd/lib/libc/net/nsparser.c")
    libbsd_use += ["yacc__nsyy"]

    # Objects built with different CFLAGS
    objs01_source = ['freebsd/bin/hostname/hostname.c',
                     'freebsd/lib/libc/gen/err.c',
                     'freebsd/lib/libc/gen/feature_present.c',
                     'freebsd/lib/libc/gen/gethostname.c',
                     'freebsd/lib/libc/gen/sethostname.c',
                     'freebsd/lib/libc/inet/inet_addr.c',
                     'freebsd/lib/libc/inet/inet_cidr_ntop.c',
                     'freebsd/lib/libc/inet/inet_cidr_pton.c',
                     'freebsd/lib/libc/inet/inet_lnaof.c',
                     'freebsd/lib/libc/inet/inet_makeaddr.c',
                     'freebsd/lib/libc/inet/inet_net_ntop.c',
                     'freebsd/lib/libc/inet/inet_net_pton.c',
                     'freebsd/lib/libc/inet/inet_neta.c',
                     'freebsd/lib/libc/inet/inet_netof.c',
                     'freebsd/lib/libc/inet/inet_network.c',
                     'freebsd/lib/libc/inet/inet_ntoa.c',
                     'freebsd/lib/libc/inet/inet_ntop.c',
                     'freebsd/lib/libc/inet/inet_pton.c',
                     'freebsd/lib/libc/inet/nsap_addr.c',
                     'freebsd/lib/libc/isc/ev_streams.c',
                     'freebsd/lib/libc/isc/ev_timers.c',
                     'freebsd/lib/libc/nameser/ns_name.c',
                     'freebsd/lib/libc/nameser/ns_netint.c',
                     'freebsd/lib/libc/nameser/ns_parse.c',
                     'freebsd/lib/libc/nameser/ns_print.c',
                     'freebsd/lib/libc/nameser/ns_samedomain.c',
                     'freebsd/lib/libc/nameser/ns_ttl.c',
                     'freebsd/lib/libc/net/base64.c',
                     'freebsd/lib/libc/net/ether_addr.c',
                     'freebsd/lib/libc/net/gai_strerror.c',
                     'freebsd/lib/libc/net/getaddrinfo.c',
                     'freebsd/lib/libc/net/gethostbydns.c',
                     'freebsd/lib/libc/net/gethostbyht.c',
                     'freebsd/lib/libc/net/gethostbynis.c',
                     'freebsd/lib/libc/net/gethostnamadr.c',
                     'freebsd/lib/libc/net/getifaddrs.c',
                     'freebsd/lib/libc/net/getifmaddrs.c',
                     'freebsd/lib/libc/net/getnameinfo.c',
                     'freebsd/lib/libc/net/getnetbydns.c',
                     'freebsd/lib/libc/net/getnetbyht.c',
                     'freebsd/lib/libc/net/getnetbynis.c',
                     'freebsd/lib/libc/net/getnetnamadr.c',
                     'freebsd/lib/libc/net/getproto.c',
                     'freebsd/lib/libc/net/getprotoent.c',
                     'freebsd/lib/libc/net/getprotoname.c',
                     'freebsd/lib/libc/net/getservent.c',
                     'freebsd/lib/libc/net/if_indextoname.c',
                     'freebsd/lib/libc/net/if_nameindex.c',
                     'freebsd/lib/libc/net/if_nametoindex.c',
                     'freebsd/lib/libc/net/ip6opt.c',
                     'freebsd/lib/libc/net/linkaddr.c',
                     'freebsd/lib/libc/net/map_v4v6.c',
                     'freebsd/lib/libc/net/name6.c',
                     'freebsd/lib/libc/net/nsdispatch.c',
                     'freebsd/lib/libc/net/rcmd.c',
                     'freebsd/lib/libc/net/recv.c',
                     'freebsd/lib/libc/net/rthdr.c',
                     'freebsd/lib/libc/net/send.c',
                     'freebsd/lib/libc/posix1e/mac.c',
                     'freebsd/lib/libc/resolv/h_errno.c',
                     'freebsd/lib/libc/resolv/herror.c',
                     'freebsd/lib/libc/resolv/mtctxres.c',
                     'freebsd/lib/libc/resolv/res_comp.c',
                     'freebsd/lib/libc/resolv/res_data.c',
                     'freebsd/lib/libc/resolv/res_debug.c',
                     'freebsd/lib/libc/resolv/res_findzonecut.c',
                     'freebsd/lib/libc/resolv/res_init.c',
                     'freebsd/lib/libc/resolv/res_mkquery.c',
                     'freebsd/lib/libc/resolv/res_mkupdate.c',
                     'freebsd/lib/libc/resolv/res_query.c',
                     'freebsd/lib/libc/resolv/res_send.c',
                     'freebsd/lib/libc/resolv/res_state.c',
                     'freebsd/lib/libc/resolv/res_update.c',
                     'freebsd/lib/libc/stdio/fgetln.c',
                     'freebsd/lib/libc/stdlib/strtonum.c',
                     'freebsd/lib/libc/string/strsep.c',
                     'freebsd/lib/libipsec/ipsec_dump_policy.c',
                     'freebsd/lib/libipsec/ipsec_get_policylen.c',
                     'freebsd/lib/libipsec/ipsec_strerror.c',
                     'freebsd/lib/libipsec/pfkey.c',
                     'freebsd/lib/libipsec/pfkey_dump.c',
                     'freebsd/lib/libmemstat/memstat.c',
                     'freebsd/lib/libmemstat/memstat_all.c',
                     'freebsd/lib/libmemstat/memstat_malloc.c',
                     'freebsd/lib/libmemstat/memstat_uma.c',
                     'freebsd/lib/libutil/expand_number.c',
                     'freebsd/lib/libutil/humanize_number.c',
                     'freebsd/lib/libutil/trimdomain.c',
                     'freebsd/sbin/dhclient/alloc.c',
                     'freebsd/sbin/dhclient/bpf.c',
                     'freebsd/sbin/dhclient/clparse.c',
                     'freebsd/sbin/dhclient/conflex.c',
                     'freebsd/sbin/dhclient/convert.c',
                     'freebsd/sbin/dhclient/dhclient.c',
                     'freebsd/sbin/dhclient/dispatch.c',
                     'freebsd/sbin/dhclient/errwarn.c',
                     'freebsd/sbin/dhclient/hash.c',
                     'freebsd/sbin/dhclient/inet.c',
                     'freebsd/sbin/dhclient/options.c',
                     'freebsd/sbin/dhclient/packet.c',
                     'freebsd/sbin/dhclient/parse.c',
                     'freebsd/sbin/dhclient/privsep.c',
                     'freebsd/sbin/dhclient/tables.c',
                     'freebsd/sbin/dhclient/tree.c',
                     'freebsd/sbin/ifconfig/af_atalk.c',
                     'freebsd/sbin/ifconfig/af_inet.c',
                     'freebsd/sbin/ifconfig/af_inet6.c',
                     'freebsd/sbin/ifconfig/af_link.c',
                     'freebsd/sbin/ifconfig/af_nd6.c',
                     'freebsd/sbin/ifconfig/ifbridge.c',
                     'freebsd/sbin/ifconfig/ifcarp.c',
                     'freebsd/sbin/ifconfig/ifclone.c',
                     'freebsd/sbin/ifconfig/ifconfig.c',
                     'freebsd/sbin/ifconfig/ifgif.c',
                     'freebsd/sbin/ifconfig/ifgre.c',
                     'freebsd/sbin/ifconfig/ifgroup.c',
                     'freebsd/sbin/ifconfig/iflagg.c',
                     'freebsd/sbin/ifconfig/ifmac.c',
                     'freebsd/sbin/ifconfig/ifmedia.c',
                     'freebsd/sbin/ifconfig/ifpfsync.c',
                     'freebsd/sbin/ifconfig/ifvlan.c',
                     'freebsd/sbin/ping/ping.c',
                     'freebsd/sbin/ping6/ping6.c',
                     'freebsd/sbin/route/route.c',
                     'freebsd/usr.bin/netstat/atalk.c',
                     'freebsd/usr.bin/netstat/bpf.c',
                     'freebsd/usr.bin/netstat/if.c',
                     'freebsd/usr.bin/netstat/inet.c',
                     'freebsd/usr.bin/netstat/inet6.c',
                     'freebsd/usr.bin/netstat/ipsec.c',
                     'freebsd/usr.bin/netstat/main.c',
                     'freebsd/usr.bin/netstat/mbuf.c',
                     'freebsd/usr.bin/netstat/mroute.c',
                     'freebsd/usr.bin/netstat/mroute6.c',
                     'freebsd/usr.bin/netstat/pfkey.c',
                     'freebsd/usr.bin/netstat/route.c',
                     'freebsd/usr.bin/netstat/sctp.c',
                     'freebsd/usr.bin/netstat/unix.c']
    bld.objects(target = "objs01",
                features = "c",
                cflags = cflags,
                includes = includes,
                defines = ['INET6'],
                source = objs01_source)
    libbsd_use += ["objs01"]

    objs02_source = ['rtemsbsd/mghttpd/mongoose.c']
    bld.objects(target = "objs02",
                features = "c",
                cflags = cflags,
                includes = includes,
                defines = ['NO_SSL', 'NO_POPEN', 'NO_CGI', 'USE_WEBSOCKET'],
                source = objs02_source)
    libbsd_use += ["objs02"]

    objs03_source = ['freebsd/lib/libc/db/btree/bt_close.c',
                     'freebsd/lib/libc/db/btree/bt_conv.c',
                     'freebsd/lib/libc/db/btree/bt_debug.c',
                     'freebsd/lib/libc/db/btree/bt_delete.c',
                     'freebsd/lib/libc/db/btree/bt_get.c',
                     'freebsd/lib/libc/db/btree/bt_open.c',
                     'freebsd/lib/libc/db/btree/bt_overflow.c',
                     'freebsd/lib/libc/db/btree/bt_page.c',
                     'freebsd/lib/libc/db/btree/bt_put.c',
                     'freebsd/lib/libc/db/btree/bt_search.c',
                     'freebsd/lib/libc/db/btree/bt_seq.c',
                     'freebsd/lib/libc/db/btree/bt_split.c',
                     'freebsd/lib/libc/db/btree/bt_utils.c',
                     'freebsd/lib/libc/db/db/db.c',
                     'freebsd/lib/libc/db/mpool/mpool-compat.c',
                     'freebsd/lib/libc/db/mpool/mpool.c',
                     'freebsd/lib/libc/db/recno/rec_close.c',
                     'freebsd/lib/libc/db/recno/rec_delete.c',
                     'freebsd/lib/libc/db/recno/rec_get.c',
                     'freebsd/lib/libc/db/recno/rec_open.c',
                     'freebsd/lib/libc/db/recno/rec_put.c',
                     'freebsd/lib/libc/db/recno/rec_search.c',
                     'freebsd/lib/libc/db/recno/rec_seq.c',
                     'freebsd/lib/libc/db/recno/rec_utils.c']
    bld.objects(target = "objs03",
                features = "c",
                cflags = cflags,
                includes = includes,
                defines = ['__DBINTERFACE_PRIVATE', 'INET6'],
                source = objs03_source)
    libbsd_use += ["objs03"]

    objs04_source = ['dhcpcd/arp.c',
                     'dhcpcd/auth.c',
                     'dhcpcd/bpf.c',
                     'dhcpcd/common.c',
                     'dhcpcd/compat/pselect.c',
                     'dhcpcd/crypt/hmac_md5.c',
                     'dhcpcd/dhcp-common.c',
                     'dhcpcd/dhcp.c',
                     'dhcpcd/dhcp6.c',
                     'dhcpcd/dhcpcd-embedded.c',
                     'dhcpcd/dhcpcd.c',
                     'dhcpcd/duid.c',
                     'dhcpcd/eloop.c',
                     'dhcpcd/if-bsd.c',
                     'dhcpcd/if-options.c',
                     'dhcpcd/if-pref.c',
                     'dhcpcd/ipv4.c',
                     'dhcpcd/ipv4ll.c',
                     'dhcpcd/ipv6.c',
                     'dhcpcd/ipv6nd.c',
                     'dhcpcd/net.c',
                     'dhcpcd/platform-bsd.c']
    bld.objects(target = "objs04",
                features = "c",
                cflags = cflags,
                includes = includes,
                defines = ['__FreeBSD__', 'THERE_IS_NO_FORK', 'MASTER_ONLY', 'INET', 'INET6'],
                source = objs04_source)
    libbsd_use += ["objs04"]

    source = ['freebsd/sys/arm/xilinx/zy7_slcr.c',
              'freebsd/sys/cam/cam.c',
              'freebsd/sys/cam/scsi/scsi_all.c',
              'freebsd/sys/contrib/altq/altq/altq_cbq.c',
              'freebsd/sys/contrib/altq/altq/altq_cdnr.c',
              'freebsd/sys/contrib/altq/altq/altq_hfsc.c',
              'freebsd/sys/contrib/altq/altq/altq_priq.c',
              'freebsd/sys/contrib/altq/altq/altq_red.c',
              'freebsd/sys/contrib/altq/altq/altq_rio.c',
              'freebsd/sys/contrib/altq/altq/altq_rmclass.c',
              'freebsd/sys/contrib/altq/altq/altq_subr.c',
              'freebsd/sys/contrib/pf/net/if_pflog.c',
              'freebsd/sys/contrib/pf/net/if_pfsync.c',
              'freebsd/sys/contrib/pf/net/pf.c',
              'freebsd/sys/contrib/pf/net/pf_if.c',
              'freebsd/sys/contrib/pf/net/pf_ioctl.c',
              'freebsd/sys/contrib/pf/net/pf_lb.c',
              'freebsd/sys/contrib/pf/net/pf_norm.c',
              'freebsd/sys/contrib/pf/net/pf_osfp.c',
              'freebsd/sys/contrib/pf/net/pf_ruleset.c',
              'freebsd/sys/contrib/pf/net/pf_table.c',
              'freebsd/sys/contrib/pf/netinet/in4_cksum.c',
              'freebsd/sys/crypto/blowfish/bf_ecb.c',
              'freebsd/sys/crypto/blowfish/bf_enc.c',
              'freebsd/sys/crypto/blowfish/bf_skey.c',
              'freebsd/sys/crypto/camellia/camellia-api.c',
              'freebsd/sys/crypto/camellia/camellia.c',
              'freebsd/sys/crypto/des/des_ecb.c',
              'freebsd/sys/crypto/des/des_enc.c',
              'freebsd/sys/crypto/des/des_setkey.c',
              'freebsd/sys/crypto/rc4/rc4.c',
              'freebsd/sys/crypto/rijndael/rijndael-alg-fst.c',
              'freebsd/sys/crypto/rijndael/rijndael-api-fst.c',
              'freebsd/sys/crypto/rijndael/rijndael-api.c',
              'freebsd/sys/crypto/sha1.c',
              'freebsd/sys/crypto/sha2/sha2.c',
              'freebsd/sys/dev/bce/if_bce.c',
              'freebsd/sys/dev/bfe/if_bfe.c',
              'freebsd/sys/dev/bge/if_bge.c',
              'freebsd/sys/dev/cadence/if_cgem.c',
              'freebsd/sys/dev/dc/dcphy.c',
              'freebsd/sys/dev/dc/if_dc.c',
              'freebsd/sys/dev/dc/pnphy.c',
              'freebsd/sys/dev/dwc/if_dwc.c',
              'freebsd/sys/dev/e1000/e1000_80003es2lan.c',
              'freebsd/sys/dev/e1000/e1000_82540.c',
              'freebsd/sys/dev/e1000/e1000_82541.c',
              'freebsd/sys/dev/e1000/e1000_82542.c',
              'freebsd/sys/dev/e1000/e1000_82543.c',
              'freebsd/sys/dev/e1000/e1000_82571.c',
              'freebsd/sys/dev/e1000/e1000_82575.c',
              'freebsd/sys/dev/e1000/e1000_api.c',
              'freebsd/sys/dev/e1000/e1000_ich8lan.c',
              'freebsd/sys/dev/e1000/e1000_mac.c',
              'freebsd/sys/dev/e1000/e1000_manage.c',
              'freebsd/sys/dev/e1000/e1000_mbx.c',
              'freebsd/sys/dev/e1000/e1000_nvm.c',
              'freebsd/sys/dev/e1000/e1000_osdep.c',
              'freebsd/sys/dev/e1000/e1000_phy.c',
              'freebsd/sys/dev/e1000/e1000_vf.c',
              'freebsd/sys/dev/e1000/if_em.c',
              'freebsd/sys/dev/e1000/if_igb.c',
              'freebsd/sys/dev/e1000/if_lem.c',
              'freebsd/sys/dev/fxp/if_fxp.c',
              'freebsd/sys/dev/led/led.c',
              'freebsd/sys/dev/mii/brgphy.c',
              'freebsd/sys/dev/mii/e1000phy.c',
              'freebsd/sys/dev/mii/icsphy.c',
              'freebsd/sys/dev/mii/micphy.c',
              'freebsd/sys/dev/mii/mii.c',
              'freebsd/sys/dev/mii/mii_bitbang.c',
              'freebsd/sys/dev/mii/mii_physubr.c',
              'freebsd/sys/dev/mii/ukphy.c',
              'freebsd/sys/dev/mii/ukphy_subr.c',
              'freebsd/sys/dev/mmc/mmc.c',
              'freebsd/sys/dev/mmc/mmcsd.c',
              'freebsd/sys/dev/pci/pci.c',
              'freebsd/sys/dev/pci/pci_pci.c',
              'freebsd/sys/dev/pci/pci_user.c',
              'freebsd/sys/dev/random/harvest.c',
              'freebsd/sys/dev/re/if_re.c',
              'freebsd/sys/dev/sdhci/sdhci.c',
              'freebsd/sys/dev/smc/if_smc.c',
              'freebsd/sys/dev/tsec/if_tsec.c',
              'freebsd/sys/dev/usb/controller/ehci.c',
              'freebsd/sys/dev/usb/controller/ohci.c',
              'freebsd/sys/dev/usb/controller/usb_controller.c',
              'freebsd/sys/dev/usb/quirk/usb_quirk.c',
              'freebsd/sys/dev/usb/storage/umass.c',
              'freebsd/sys/dev/usb/usb_busdma.c',
              'freebsd/sys/dev/usb/usb_core.c',
              'freebsd/sys/dev/usb/usb_debug.c',
              'freebsd/sys/dev/usb/usb_dev.c',
              'freebsd/sys/dev/usb/usb_device.c',
              'freebsd/sys/dev/usb/usb_dynamic.c',
              'freebsd/sys/dev/usb/usb_error.c',
              'freebsd/sys/dev/usb/usb_generic.c',
              'freebsd/sys/dev/usb/usb_handle_request.c',
              'freebsd/sys/dev/usb/usb_hid.c',
              'freebsd/sys/dev/usb/usb_hub.c',
              'freebsd/sys/dev/usb/usb_lookup.c',
              'freebsd/sys/dev/usb/usb_mbuf.c',
              'freebsd/sys/dev/usb/usb_msctest.c',
              'freebsd/sys/dev/usb/usb_parse.c',
              'freebsd/sys/dev/usb/usb_process.c',
              'freebsd/sys/dev/usb/usb_request.c',
              'freebsd/sys/dev/usb/usb_transfer.c',
              'freebsd/sys/dev/usb/usb_util.c',
              'freebsd/sys/kern/init_main.c',
              'freebsd/sys/kern/kern_condvar.c',
              'freebsd/sys/kern/kern_event.c',
              'freebsd/sys/kern/kern_hhook.c',
              'freebsd/sys/kern/kern_intr.c',
              'freebsd/sys/kern/kern_khelp.c',
              'freebsd/sys/kern/kern_linker.c',
              'freebsd/sys/kern/kern_mbuf.c',
              'freebsd/sys/kern/kern_mib.c',
              'freebsd/sys/kern/kern_module.c',
              'freebsd/sys/kern/kern_mtxpool.c',
              'freebsd/sys/kern/kern_osd.c',
              'freebsd/sys/kern/kern_synch.c',
              'freebsd/sys/kern/kern_sysctl.c',
              'freebsd/sys/kern/kern_time.c',
              'freebsd/sys/kern/kern_timeout.c',
              'freebsd/sys/kern/subr_bufring.c',
              'freebsd/sys/kern/subr_bus.c',
              'freebsd/sys/kern/subr_eventhandler.c',
              'freebsd/sys/kern/subr_hash.c',
              'freebsd/sys/kern/subr_hints.c',
              'freebsd/sys/kern/subr_kobj.c',
              'freebsd/sys/kern/subr_lock.c',
              'freebsd/sys/kern/subr_module.c',
              'freebsd/sys/kern/subr_rman.c',
              'freebsd/sys/kern/subr_sbuf.c',
              'freebsd/sys/kern/subr_sleepqueue.c',
              'freebsd/sys/kern/subr_taskqueue.c',
              'freebsd/sys/kern/subr_uio.c',
              'freebsd/sys/kern/subr_unit.c',
              'freebsd/sys/kern/sys_generic.c',
              'freebsd/sys/kern/sys_socket.c',
              'freebsd/sys/kern/uipc_accf.c',
              'freebsd/sys/kern/uipc_domain.c',
              'freebsd/sys/kern/uipc_mbuf.c',
              'freebsd/sys/kern/uipc_mbuf2.c',
              'freebsd/sys/kern/uipc_sockbuf.c',
              'freebsd/sys/kern/uipc_socket.c',
              'freebsd/sys/kern/uipc_syscalls.c',
              'freebsd/sys/kern/uipc_usrreq.c',
              'freebsd/sys/libkern/arc4random.c',
              'freebsd/sys/libkern/fls.c',
              'freebsd/sys/libkern/inet_ntoa.c',
              'freebsd/sys/libkern/random.c',
              'freebsd/sys/net/bpf.c',
              'freebsd/sys/net/bpf_buffer.c',
              'freebsd/sys/net/bpf_filter.c',
              'freebsd/sys/net/bpf_jitter.c',
              'freebsd/sys/net/bridgestp.c',
              'freebsd/sys/net/ieee8023ad_lacp.c',
              'freebsd/sys/net/if.c',
              'freebsd/sys/net/if_arcsubr.c',
              'freebsd/sys/net/if_atmsubr.c',
              'freebsd/sys/net/if_bridge.c',
              'freebsd/sys/net/if_clone.c',
              'freebsd/sys/net/if_dead.c',
              'freebsd/sys/net/if_disc.c',
              'freebsd/sys/net/if_edsc.c',
              'freebsd/sys/net/if_ef.c',
              'freebsd/sys/net/if_enc.c',
              'freebsd/sys/net/if_epair.c',
              'freebsd/sys/net/if_ethersubr.c',
              'freebsd/sys/net/if_faith.c',
              'freebsd/sys/net/if_fddisubr.c',
              'freebsd/sys/net/if_fwsubr.c',
              'freebsd/sys/net/if_gif.c',
              'freebsd/sys/net/if_gre.c',
              'freebsd/sys/net/if_iso88025subr.c',
              'freebsd/sys/net/if_lagg.c',
              'freebsd/sys/net/if_llatbl.c',
              'freebsd/sys/net/if_loop.c',
              'freebsd/sys/net/if_media.c',
              'freebsd/sys/net/if_mib.c',
              'freebsd/sys/net/if_spppfr.c',
              'freebsd/sys/net/if_spppsubr.c',
              'freebsd/sys/net/if_stf.c',
              'freebsd/sys/net/if_tap.c',
              'freebsd/sys/net/if_tun.c',
              'freebsd/sys/net/if_vlan.c',
              'freebsd/sys/net/netisr.c',
              'freebsd/sys/net/pfil.c',
              'freebsd/sys/net/radix.c',
              'freebsd/sys/net/radix_mpath.c',
              'freebsd/sys/net/raw_cb.c',
              'freebsd/sys/net/raw_usrreq.c',
              'freebsd/sys/net/route.c',
              'freebsd/sys/net/rtsock.c',
              'freebsd/sys/net/slcompress.c',
              'freebsd/sys/netatalk/aarp.c',
              'freebsd/sys/netatalk/at_control.c',
              'freebsd/sys/netatalk/at_proto.c',
              'freebsd/sys/netatalk/at_rmx.c',
              'freebsd/sys/netatalk/ddp_input.c',
              'freebsd/sys/netatalk/ddp_output.c',
              'freebsd/sys/netatalk/ddp_pcb.c',
              'freebsd/sys/netatalk/ddp_usrreq.c',
              'freebsd/sys/netinet/accf_data.c',
              'freebsd/sys/netinet/accf_dns.c',
              'freebsd/sys/netinet/accf_http.c',
              'freebsd/sys/netinet/cc/cc.c',
              'freebsd/sys/netinet/cc/cc_newreno.c',
              'freebsd/sys/netinet/if_atm.c',
              'freebsd/sys/netinet/if_ether.c',
              'freebsd/sys/netinet/igmp.c',
              'freebsd/sys/netinet/in.c',
              'freebsd/sys/netinet/in_gif.c',
              'freebsd/sys/netinet/in_mcast.c',
              'freebsd/sys/netinet/in_pcb.c',
              'freebsd/sys/netinet/in_proto.c',
              'freebsd/sys/netinet/in_rmx.c',
              'freebsd/sys/netinet/ip_carp.c',
              'freebsd/sys/netinet/ip_divert.c',
              'freebsd/sys/netinet/ip_ecn.c',
              'freebsd/sys/netinet/ip_encap.c',
              'freebsd/sys/netinet/ip_fastfwd.c',
              'freebsd/sys/netinet/ip_gre.c',
              'freebsd/sys/netinet/ip_icmp.c',
              'freebsd/sys/netinet/ip_id.c',
              'freebsd/sys/netinet/ip_input.c',
              'freebsd/sys/netinet/ip_mroute.c',
              'freebsd/sys/netinet/ip_options.c',
              'freebsd/sys/netinet/ip_output.c',
              'freebsd/sys/netinet/libalias/alias.c',
              'freebsd/sys/netinet/libalias/alias_cuseeme.c',
              'freebsd/sys/netinet/libalias/alias_db.c',
              'freebsd/sys/netinet/libalias/alias_dummy.c',
              'freebsd/sys/netinet/libalias/alias_ftp.c',
              'freebsd/sys/netinet/libalias/alias_irc.c',
              'freebsd/sys/netinet/libalias/alias_mod.c',
              'freebsd/sys/netinet/libalias/alias_nbt.c',
              'freebsd/sys/netinet/libalias/alias_pptp.c',
              'freebsd/sys/netinet/libalias/alias_proxy.c',
              'freebsd/sys/netinet/libalias/alias_sctp.c',
              'freebsd/sys/netinet/libalias/alias_skinny.c',
              'freebsd/sys/netinet/libalias/alias_smedia.c',
              'freebsd/sys/netinet/libalias/alias_util.c',
              'freebsd/sys/netinet/raw_ip.c',
              'freebsd/sys/netinet/sctp_asconf.c',
              'freebsd/sys/netinet/sctp_auth.c',
              'freebsd/sys/netinet/sctp_bsd_addr.c',
              'freebsd/sys/netinet/sctp_cc_functions.c',
              'freebsd/sys/netinet/sctp_crc32.c',
              'freebsd/sys/netinet/sctp_indata.c',
              'freebsd/sys/netinet/sctp_input.c',
              'freebsd/sys/netinet/sctp_output.c',
              'freebsd/sys/netinet/sctp_pcb.c',
              'freebsd/sys/netinet/sctp_peeloff.c',
              'freebsd/sys/netinet/sctp_sysctl.c',
              'freebsd/sys/netinet/sctp_timer.c',
              'freebsd/sys/netinet/sctp_usrreq.c',
              'freebsd/sys/netinet/sctputil.c',
              'freebsd/sys/netinet/tcp_debug.c',
              'freebsd/sys/netinet/tcp_hostcache.c',
              'freebsd/sys/netinet/tcp_input.c',
              'freebsd/sys/netinet/tcp_lro.c',
              'freebsd/sys/netinet/tcp_offload.c',
              'freebsd/sys/netinet/tcp_output.c',
              'freebsd/sys/netinet/tcp_reass.c',
              'freebsd/sys/netinet/tcp_sack.c',
              'freebsd/sys/netinet/tcp_subr.c',
              'freebsd/sys/netinet/tcp_syncache.c',
              'freebsd/sys/netinet/tcp_timer.c',
              'freebsd/sys/netinet/tcp_timewait.c',
              'freebsd/sys/netinet/tcp_usrreq.c',
              'freebsd/sys/netinet/udp_usrreq.c',
              'freebsd/sys/netinet6/dest6.c',
              'freebsd/sys/netinet6/frag6.c',
              'freebsd/sys/netinet6/icmp6.c',
              'freebsd/sys/netinet6/in6.c',
              'freebsd/sys/netinet6/in6_cksum.c',
              'freebsd/sys/netinet6/in6_gif.c',
              'freebsd/sys/netinet6/in6_ifattach.c',
              'freebsd/sys/netinet6/in6_mcast.c',
              'freebsd/sys/netinet6/in6_pcb.c',
              'freebsd/sys/netinet6/in6_proto.c',
              'freebsd/sys/netinet6/in6_rmx.c',
              'freebsd/sys/netinet6/in6_src.c',
              'freebsd/sys/netinet6/ip6_forward.c',
              'freebsd/sys/netinet6/ip6_id.c',
              'freebsd/sys/netinet6/ip6_input.c',
              'freebsd/sys/netinet6/ip6_mroute.c',
              'freebsd/sys/netinet6/ip6_output.c',
              'freebsd/sys/netinet6/mld6.c',
              'freebsd/sys/netinet6/nd6.c',
              'freebsd/sys/netinet6/nd6_nbr.c',
              'freebsd/sys/netinet6/nd6_rtr.c',
              'freebsd/sys/netinet6/raw_ip6.c',
              'freebsd/sys/netinet6/route6.c',
              'freebsd/sys/netinet6/scope6.c',
              'freebsd/sys/netinet6/sctp6_usrreq.c',
              'freebsd/sys/netinet6/udp6_usrreq.c',
              'freebsd/sys/netpfil/ipfw/dn_heap.c',
              'freebsd/sys/netpfil/ipfw/dn_sched_fifo.c',
              'freebsd/sys/netpfil/ipfw/dn_sched_prio.c',
              'freebsd/sys/netpfil/ipfw/dn_sched_qfq.c',
              'freebsd/sys/netpfil/ipfw/dn_sched_rr.c',
              'freebsd/sys/netpfil/ipfw/dn_sched_wf2q.c',
              'freebsd/sys/netpfil/ipfw/ip_dn_glue.c',
              'freebsd/sys/netpfil/ipfw/ip_dn_io.c',
              'freebsd/sys/netpfil/ipfw/ip_dummynet.c',
              'freebsd/sys/netpfil/ipfw/ip_fw2.c',
              'freebsd/sys/netpfil/ipfw/ip_fw_log.c',
              'freebsd/sys/netpfil/ipfw/ip_fw_nat.c',
              'freebsd/sys/netpfil/ipfw/ip_fw_pfil.c',
              'freebsd/sys/netpfil/ipfw/ip_fw_sockopt.c',
              'freebsd/sys/netpfil/ipfw/ip_fw_table.c',
              'freebsd/sys/opencrypto/cast.c',
              'freebsd/sys/opencrypto/criov.c',
              'freebsd/sys/opencrypto/crypto.c',
              'freebsd/sys/opencrypto/cryptosoft.c',
              'freebsd/sys/opencrypto/deflate.c',
              'freebsd/sys/opencrypto/rmd160.c',
              'freebsd/sys/opencrypto/skipjack.c',
              'freebsd/sys/opencrypto/xform.c',
              'freebsd/sys/vm/uma_core.c',
              'mDNSResponder/mDNSCore/CryptoAlg.c',
              'mDNSResponder/mDNSCore/DNSCommon.c',
              'mDNSResponder/mDNSCore/DNSDigest.c',
              'mDNSResponder/mDNSCore/anonymous.c',
              'mDNSResponder/mDNSCore/mDNS.c',
              'mDNSResponder/mDNSCore/uDNS.c',
              'mDNSResponder/mDNSPosix/mDNSPosix.c',
              'mDNSResponder/mDNSPosix/mDNSUNP.c',
              'mDNSResponder/mDNSShared/GenLinkedList.c',
              'mDNSResponder/mDNSShared/PlatformCommon.c',
              'mDNSResponder/mDNSShared/dnssd_clientshim.c',
              'mDNSResponder/mDNSShared/mDNSDebug.c',
              'rtemsbsd/ftpd/ftpd.c',
              'rtemsbsd/local/bus_if.c',
              'rtemsbsd/local/cryptodev_if.c',
              'rtemsbsd/local/device_if.c',
              'rtemsbsd/local/miibus_if.c',
              'rtemsbsd/local/mmcbr_if.c',
              'rtemsbsd/local/mmcbus_if.c',
              'rtemsbsd/local/pci_if.c',
              'rtemsbsd/local/pcib_if.c',
              'rtemsbsd/local/usb_if.c',
              'rtemsbsd/mdns/mdns-hostname-default.c',
              'rtemsbsd/mdns/mdns.c',
              'rtemsbsd/pppd/auth.c',
              'rtemsbsd/pppd/ccp.c',
              'rtemsbsd/pppd/chap.c',
              'rtemsbsd/pppd/chap_ms.c',
              'rtemsbsd/pppd/chat.c',
              'rtemsbsd/pppd/demand.c',
              'rtemsbsd/pppd/fsm.c',
              'rtemsbsd/pppd/ipcp.c',
              'rtemsbsd/pppd/lcp.c',
              'rtemsbsd/pppd/magic.c',
              'rtemsbsd/pppd/options.c',
              'rtemsbsd/pppd/rtemsmain.c',
              'rtemsbsd/pppd/rtemspppd.c',
              'rtemsbsd/pppd/sys-rtems.c',
              'rtemsbsd/pppd/upap.c',
              'rtemsbsd/pppd/utils.c',
              'rtemsbsd/rtems/ipsec_get_policylen.c',
              'rtemsbsd/rtems/rtems-bsd-arp-processor.c',
              'rtemsbsd/rtems/rtems-bsd-assert.c',
              'rtemsbsd/rtems/rtems-bsd-autoconf.c',
              'rtemsbsd/rtems/rtems-bsd-bus-dma-mbuf.c',
              'rtemsbsd/rtems/rtems-bsd-bus-dma.c',
              'rtemsbsd/rtems/rtems-bsd-cam.c',
              'rtemsbsd/rtems/rtems-bsd-chunk.c',
              'rtemsbsd/rtems/rtems-bsd-conf.c',
              'rtemsbsd/rtems/rtems-bsd-configintrhook.c',
              'rtemsbsd/rtems/rtems-bsd-delay.c',
              'rtemsbsd/rtems/rtems-bsd-get-allocator-domain-size.c',
              'rtemsbsd/rtems/rtems-bsd-get-ethernet-addr.c',
              'rtemsbsd/rtems/rtems-bsd-get-file.c',
              'rtemsbsd/rtems/rtems-bsd-get-mac-address.c',
              'rtemsbsd/rtems/rtems-bsd-get-task-priority.c',
              'rtemsbsd/rtems/rtems-bsd-get-task-stack-size.c',
              'rtemsbsd/rtems/rtems-bsd-init.c',
              'rtemsbsd/rtems/rtems-bsd-jail.c',
              'rtemsbsd/rtems/rtems-bsd-log.c',
              'rtemsbsd/rtems/rtems-bsd-malloc.c',
              'rtemsbsd/rtems/rtems-bsd-mbuf.c',
              'rtemsbsd/rtems/rtems-bsd-mutex.c',
              'rtemsbsd/rtems/rtems-bsd-muteximpl.c',
              'rtemsbsd/rtems/rtems-bsd-newproc.c',
              'rtemsbsd/rtems/rtems-bsd-nexus.c',
              'rtemsbsd/rtems/rtems-bsd-page.c',
              'rtemsbsd/rtems/rtems-bsd-panic.c',
              'rtemsbsd/rtems/rtems-bsd-pci_bus.c',
              'rtemsbsd/rtems/rtems-bsd-pci_cfgreg.c',
              'rtemsbsd/rtems/rtems-bsd-program.c',
              'rtemsbsd/rtems/rtems-bsd-rwlock.c',
              'rtemsbsd/rtems/rtems-bsd-shell-dhcpcd.c',
              'rtemsbsd/rtems/rtems-bsd-shell-netcmds.c',
              'rtemsbsd/rtems/rtems-bsd-shell.c',
              'rtemsbsd/rtems/rtems-bsd-signal.c',
              'rtemsbsd/rtems/rtems-bsd-sx.c',
              'rtemsbsd/rtems/rtems-bsd-syscall-api.c',
              'rtemsbsd/rtems/rtems-bsd-sysctl.c',
              'rtemsbsd/rtems/rtems-bsd-sysctlbyname.c',
              'rtemsbsd/rtems/rtems-bsd-sysctlnametomib.c',
              'rtemsbsd/rtems/rtems-bsd-thread.c',
              'rtemsbsd/rtems/rtems-bsd-timesupport.c',
              'rtemsbsd/rtems/rtems-bsdnet-rtrequest.c',
              'rtemsbsd/rtems/rtems-kvm.c',
              'rtemsbsd/rtems/rtems-syslog-initialize.c',
              'rtemsbsd/rtems/rtems_mii_ioctl_kern.c',
              'rtemsbsd/rtems/syslog.c',
              'rtemsbsd/sys/dev/dw_mmc/dw_mmc.c',
              'rtemsbsd/sys/dev/ffec/if_ffec_mcf548x.c',
              'rtemsbsd/sys/dev/smc/if_smc_nexus.c',
              'rtemsbsd/sys/dev/tsec/if_tsec_nexus.c',
              'rtemsbsd/sys/dev/usb/controller/ehci_mpc83xx.c',
              'rtemsbsd/sys/dev/usb/controller/ohci_lpc.c',
              'rtemsbsd/sys/dev/usb/controller/usb_otg_transceiver.c',
              'rtemsbsd/sys/dev/usb/controller/usb_otg_transceiver_dump.c',
              'rtemsbsd/sys/net/if_ppp.c',
              'rtemsbsd/sys/net/ppp_tty.c',
              'rtemsbsd/telnetd/check_passwd.c',
              'rtemsbsd/telnetd/des.c',
              'rtemsbsd/telnetd/pty.c',
              'rtemsbsd/telnetd/telnetd.c']
    if bld.get_env()["RTEMS_ARCH"] == "arm":
        source += ['freebsd/sys/arm/arm/in_cksum.c',
                   'freebsd/sys/arm/arm/legacy.c',
                   'freebsd/sys/arm/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "avr":
        source += ['freebsd/sys/avr/avr/in_cksum.c',
                   'freebsd/sys/avr/avr/legacy.c',
                   'freebsd/sys/avr/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "bfin":
        source += ['freebsd/sys/bfin/bfin/in_cksum.c',
                   'freebsd/sys/bfin/bfin/legacy.c',
                   'freebsd/sys/bfin/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "h8300":
        source += ['freebsd/sys/h8300/h8300/in_cksum.c',
                   'freebsd/sys/h8300/h8300/legacy.c',
                   'freebsd/sys/h8300/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "i386":
        source += ['freebsd/sys/i386/i386/in_cksum.c',
                   'freebsd/sys/i386/i386/legacy.c',
                   'freebsd/sys/i386/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "lm32":
        source += ['freebsd/sys/lm32/lm32/in_cksum.c',
                   'freebsd/sys/lm32/lm32/legacy.c',
                   'freebsd/sys/lm32/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "m32c":
        source += ['freebsd/sys/m32c/m32c/in_cksum.c',
                   'freebsd/sys/m32c/m32c/legacy.c',
                   'freebsd/sys/m32c/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "m32r":
        source += ['freebsd/sys/m32r/m32r/in_cksum.c',
                   'freebsd/sys/m32r/m32r/legacy.c',
                   'freebsd/sys/m32r/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "m68k":
        source += ['freebsd/sys/m68k/m68k/in_cksum.c',
                   'freebsd/sys/m68k/m68k/legacy.c',
                   'freebsd/sys/m68k/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "mips":
        source += ['freebsd/sys/mips/mips/in_cksum.c',
                   'freebsd/sys/mips/mips/legacy.c',
                   'freebsd/sys/mips/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "nios2":
        source += ['freebsd/sys/nios2/nios2/in_cksum.c',
                   'freebsd/sys/nios2/nios2/legacy.c',
                   'freebsd/sys/nios2/pci/pci_bus.c']
    if bld.get_env()["RTEMS_ARCH"] == "powerpc":
        source += ['freebsd/sys/powerpc/pci/pci_bus.c',
                   'freebsd/sys/powerpc/powerpc/in_cksum.c',
                   'freebsd/sys/powerpc/powerpc/legacy.c']
    if bld.get_env()["RTEMS_ARCH"] == "sh":
        source += ['freebsd/sys/sh/pci/pci_bus.c',
                   'freebsd/sys/sh/sh/in_cksum.c',
                   'freebsd/sys/sh/sh/legacy.c']
    if bld.get_env()["RTEMS_ARCH"] == "sparc":
        source += ['freebsd/sys/mips/mips/in_cksum.c',
                   'freebsd/sys/sparc/pci/pci_bus.c',
                   'freebsd/sys/sparc/sparc/in_cksum.c',
                   'freebsd/sys/sparc/sparc/legacy.c']
    if bld.get_env()["RTEMS_ARCH"] == "sparc64":
        source += ['freebsd/sys/sparc64/pci/pci_bus.c',
                   'freebsd/sys/sparc64/sparc64/in_cksum.c',
                   'freebsd/sys/sparc64/sparc64/legacy.c']
    if bld.get_env()["RTEMS_ARCH"] == "v850":
        source += ['freebsd/sys/v850/pci/pci_bus.c',
                   'freebsd/sys/v850/v850/in_cksum.c',
                   'freebsd/sys/v850/v850/legacy.c']
    bld.stlib(target = "bsd",
              features = "c cxx",
              cflags = cflags,
              cxxflags = cxxflags,
              includes = includes,
              source = source,
              use = libbsd_use)

    # Tests
    test_init01 = ['testsuite/init01/test_main.c']
    bld.program(target = "init01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_init01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_syscalls01 = ['testsuite/syscalls01/test_main.c']
    bld.program(target = "syscalls01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_syscalls01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_thread01 = ['testsuite/thread01/test_main.c']
    bld.program(target = "thread01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_thread01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_loopback01 = ['testsuite/loopback01/test_main.c']
    bld.program(target = "loopback01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_loopback01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_foobarclient = ['testsuite/foobarclient/test_main.c']
    bld.program(target = "foobarclient",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_foobarclient,
                use = ["bsd"],
                lib = ["m", "z"])

    test_lagg01 = ['testsuite/lagg01/test_main.c']
    bld.program(target = "lagg01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_lagg01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_timeout01 = ['testsuite/timeout01/init.c',
                      'testsuite/timeout01/timeout_test.c']
    bld.program(target = "timeout01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_timeout01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_dhcpcd02 = ['testsuite/dhcpcd02/test_main.c']
    bld.program(target = "dhcpcd02",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_dhcpcd02,
                use = ["bsd"],
                lib = ["m", "z"])

    test_ftpd01 = ['testsuite/ftpd01/test_main.c']
    bld.program(target = "ftpd01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_ftpd01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_vlan01 = ['testsuite/vlan01/test_main.c']
    bld.program(target = "vlan01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_vlan01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_foobarserver = ['testsuite/foobarserver/test_main.c']
    bld.program(target = "foobarserver",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_foobarserver,
                use = ["bsd"],
                lib = ["m", "z"])

    test_selectpollkqueue01 = ['testsuite/selectpollkqueue01/test_main.c']
    bld.program(target = "selectpollkqueue01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_selectpollkqueue01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_zerocopy01 = ['testsuite/zerocopy01/test_main.c']
    bld.program(target = "zerocopy01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_zerocopy01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_smp01 = ['testsuite/smp01/test_main.c']
    bld.program(target = "smp01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_smp01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_media01 = ['testsuite/media01/test_main.c']
    bld.program(target = "media01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_media01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_condvar01 = ['testsuite/condvar01/test_main.c']
    bld.program(target = "condvar01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_condvar01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_telnetd01 = ['testsuite/telnetd01/test_main.c']
    bld.program(target = "telnetd01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_telnetd01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_ppp01 = ['testsuite/ppp01/test_main.c']
    bld.program(target = "ppp01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_ppp01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_swi01 = ['testsuite/swi01/init.c',
                  'testsuite/swi01/swi_test.c']
    bld.program(target = "swi01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_swi01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_netshell01 = ['testsuite/netshell01/shellconfig.c',
                       'testsuite/netshell01/test_main.c']
    bld.program(target = "netshell01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_netshell01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_rwlock01 = ['testsuite/rwlock01/test_main.c']
    bld.program(target = "rwlock01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_rwlock01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_mutex01 = ['testsuite/mutex01/test_main.c']
    bld.program(target = "mutex01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_mutex01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_dhcpcd01 = ['testsuite/dhcpcd01/test_main.c']
    bld.program(target = "dhcpcd01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_dhcpcd01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_unix01 = ['testsuite/unix01/test_main.c']
    bld.program(target = "unix01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_unix01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_commands01 = ['testsuite/commands01/test_main.c']
    bld.program(target = "commands01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_commands01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_ping01 = ['testsuite/ping01/test_main.c']
    bld.program(target = "ping01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_ping01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_usb01 = ['testsuite/usb01/init.c',
                  'testsuite/usb01/test-file-system.c']
    bld.program(target = "usb01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_usb01,
                use = ["bsd"],
                lib = ["m", "z"])

    test_arphole = ['testsuite/arphole/test_main.c']
    bld.program(target = "arphole",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_arphole,
                use = ["bsd"],
                lib = ["m", "z"])

    test_sleep01 = ['testsuite/sleep01/test_main.c']
    bld.program(target = "sleep01",
                features = "cprogram",
                cflags = cflags,
                includes = includes,
                source = test_sleep01,
                use = ["bsd"],
                lib = ["m", "z"])

