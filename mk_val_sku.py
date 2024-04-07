
import json

def main():
    input_json = './annotations/base_val.json'
    output_json = './sku_val.json'
    csv_file = './annotations/annotations_val.csv'

    with open(input_json, 'r') as f:
        coco_annotations = json.load(f)

    ann_list = []
    img_list= []
    img_id_list = []
    max_img_id = 0
    with open(csv_file, 'r') as fp_r:
        for line in fp_r:
            line_sp = line.split(',')
            # name, x1, y1, x2, y2, class, img_w, img_h
            img_id = line_sp[0]
            img_id = img_id.split('.')[0]
            img_id = img_id.split('val_')[1]
            img_id = int(img_id.zfill(6))
            if img_id > max_img_id:
                max_img_id = img_id

            data = {}
            data['img_id'] = img_id
            data['name'] = line_sp[0]
            x1 = float(line_sp[1])
            y1 = float(line_sp[2])
            x2 = float(line_sp[3])
            y2 = float(line_sp[4])
            w = x2 - x1
            h = y2 - y1
            data['x'] = x1
            data['y'] = y1
            data['w'] = w
            data['h'] = h
            data['cls'] = line_sp[5]
            assert data['cls'] == 'object'
            data['img_w'] = line_sp[6]
            data['img_h'] = line_sp[7]
            ann_list.append(data)

            img_data = {}

            img_data['img_id'] = img_id
            img_data['name'] = line_sp[0]
            img_data['w'] = int(line_sp[6])
            img_data['h'] = int(line_sp[7].strip())

            if not img_id in img_id_list:
                img_id_list.append(img_id)
                img_list.append(img_data)
            else:
                hit = False
                for aaa , bbb in zip(img_id_list, img_list):
                    if aaa == img_id:
                        assert bbb['img_id'] == img_data['img_id']
                        assert bbb['name'] == img_data['name']
                        assert bbb['w'] == img_data['w']
                        assert bbb['h'] == img_data['h']
                        hit = True
                        break
                assert hit == True

    #import ipdb;ipdb.set_trace()
    bk_images = coco_annotations['images']
    images = []
    for img in img_list:
        img_dict = {}
        img_dict['license'] = 4;    # TODO
        img_dict['filename'] = img['name']
        img_dict['height'] = img['h']
        img_dict['width'] = img['w']
        img_dict['id'] = img['img_id']
        images.append(img_dict)
    coco_annotations['images'] = images

    bk_annotations = coco_annotations['annotations']
    annotations = []

    for index, ann in enumerate(ann_list):
        ann_dict = {}
        ann_dict['iscrowd'] = 0
        ann_dict['image_id'] = ann['img_id']
        ann_dict['category_id'] = 18    # TODO
        bbox = [ann['x'], ann['y'], ann['w'], ann['h']]
        ann_dict['bbox'] = bbox
        ann_dict['id'] = max_img_id + index + 1
        annotations.append(ann_dict)
    coco_annotations['annotations'] = annotations

    with open(output_json, 'w') as fp_w:
        json.dump(coco_annotations, fp_w, sort_keys=True, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
