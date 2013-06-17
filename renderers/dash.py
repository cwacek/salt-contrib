from __future__ import absolute_import
import yaml
import salt.utils.templates
from salt.exceptions import SaltRenderError

def render(template, env='', sls='', sources={'grains':__grains__}, **kws):
  """
  Dash is a basic YAML renderer designed to 
  enable simple inline switch statements that can
  be used to use different data for different
  configurations.

  Dash switch statements are YAML keys which begin
  with '@', and take the form '@<datasource>.<key>'.
  Dash will look for <key> in the specified source - 
  the default source is just Grains, but additional
  can be specified in the :sources: argument.

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
  """

  data = yaml.load(template)
  pillar = convert(data)
  return pillar

def get_filter_val(f):
  f = f[1:]
  modules = f.split(".")
  if modules[0] not in sources:
    raise SaltRenderError("Requested filter module '{0}' could not be found")

  try:
    return sources[modules[0]][modules[1]]
  except KeyError:
    raise SaltRenderError("Grains filter '{0}' could not be found"
                          .format(modules[1]))

def convert(source):

  if isinstance(source,(list)):
    return [convert(elem) for elem in source]

  if isinstance(source,(basestring,int,float)):
    return source

  # It's a dict, so handle special
  pillar_data = dict()
  for key in source:
    if key[0] != '@':
      pillar_data[key] = convert(source[key])
    else:
      if 'default' not in source[key]:
        raise SaltRenderError("'default' values required for switch value")

      pillar_data = convert(source[key]['default'])
      target = get_filter_val(key)

      if isinstance(source[key]['default'],(dict)):
        for subkey in source[key].get(target,[]):
          print("Converting dict or literal {0}".format(key))
          pillar_data[subkey] = convert(source[key][target][subkey])
      else:
        # Lists are a little special
        for i,elem in enumerate(source[key].get(target,[])):
          if (i < len(pillar_data)):
            pillar_data[i] = convert(source[key][target][i])
          else:
            pillar_data.append(convert(source[key][target][i]) )

  return pillar_data
