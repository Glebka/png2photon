meta:
  id: pmse
  file-extension: Photon Mono SE format
  endian: le
seq:
  - id: magic
    size: 12
  - id: version
    type: u4
  - id: area_num
    type: u4
  - id: header_addr
    type: u4
  - id: back0
    size: 4
  - id: preview_addr
    type: u4
  - id: back1
    size: 4
  - id: layersdef_addr
    type: u4
  - id: back2
    size: 4
  - id: layers_image_addr
    type: u4
  - id: header
    type: header
instances:
  preview:
    pos: preview_addr
    type: preview
  layersdef:
    pos: layersdef_addr
    type: layersdef
types:
  header:
    seq:
      - id: marker
        size: 12
      - id: len
        type: s4le
      - id: pixel_size
        type: f4
      - id: layer_thikness
        type: f4
      - id: normal_exp_time
        type: f4
      - id: uv_off_time
        type: f4
      - id: bottom_exp_time
        type: f4
      - id: bottom_layers
        type: f4
      - id: z_lift_height
        type: f4
      - id: z_lift_up_speed
        type: f4
      - id: z_lift_down_speed
        type: f4
      - id: volume
        type: f4
      - id: anti_aliasing_grade
        type: s4
      - id: res_x
        type: u4
      - id: res_y
        type: u4
      - id: weight
        type: f4
      - id: price
        type: f4
      - id: resin_type
        type: u4
      - id: use_individual_param
        type: u4
      - id: reserved
        size: 3*4
      
  preview:
    seq:
      - id: marker
        size: 12
      - id: size
        type: u4
      - id: width
        type: u4
      - id: mark
        size: 4
      - id: height
        type: u4
      - id: image_data
        size: 2*width*height
  layersdef:
    seq:
      - id: marker
        size: 12
      - id: size
        type: u4
      - id: layers_count
        type: u4
      - id: layer_def
        type: layer_def
        repeat: expr
        repeat-expr: layers_count
  layer_def:
    seq:
      - id: addr
        type: u4
      - id: size
        type: u4
      - id: z_lift_height
        type: f4
      - id: z_lift_speed
        type: f4
      - id: exp_time
        type: f4
      - id: backup
        size: 12
    instances:
      data:
        pos: addr
        size: size