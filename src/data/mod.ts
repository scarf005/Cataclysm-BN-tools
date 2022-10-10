type ModType =
  | 'content'
  | 'items'
  | 'creatures'
  | 'misc_additions'
  | 'buildings'
  | 'vehicles'
  | 'rebalance'
  | 'magical'
  | 'item_exclude'
  | 'monster_exclude'
  | 'graphical'

export interface ModSchema {
  type: string
  id: string
  name: string
  description: string
  category: string
  core: boolean
  path: string
}
