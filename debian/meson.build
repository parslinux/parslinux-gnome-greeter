version_target = custom_target(
    'debian-version',
    output: '__version__',
    input: 'changelog',
    command: ['bash', '-c', 'head -n 1 @INPUT@ | sed "s/.*(//g;s/).*//g" > @OUTPUT@'],
    install: true,
    install_dir: '/usr/share/parslinux/parslinux-gnome-greeter'
)

