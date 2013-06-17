### Dash Renderer

Dash is a basic YAML renderer designed to
enable simple inline switch statements that can
be used to use different data for different
configurations.

Dash switch statements are YAML keys which begin
with '@', and take the form `@<datasource>.<key>`.
Dash will look for *key* in the specified source -
the default source is just Grains, but additional
can be specified in the *sources* argument.

For each Dash switch, one of the keys must be
'default'. These values will be used if nothing
else matches the switch.

    vim:
      pkg.installed:
        '@grains.os_family':
          RedHat:
            - name: vim-common
          default:
            - name: vim

The example above switches the name of the 'vim'
package depending on the OS family.

