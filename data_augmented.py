import os
import cv2
import imgaug.augmenters as iaa
import numpy as np

def load_images_from_folder(folder):
    """Carrega todas as imagens de uma pasta."""
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append((filename, img))
    return images

def augment_images(images, augmenter, prefix="aug_"):
    """Aplica data augmentation a uma lista de imagens e adiciona um prefixo aos nomes."""
    augmented_images = []
    for name, img in images:
        # Aplica a augmentação normal
        augmented_img = augmenter(image=img)
        augmented_name = f"{prefix}{name}"
        augmented_images.append((augmented_name, augmented_img))
        
        # Aplica a inversão horizontal (flip)
        flipped_img = np.fliplr(img)  # Flip horizontal
        flipped_name = f"{prefix}flip_{name}"
        augmented_images.append((flipped_name, flipped_img))
        
    return augmented_images

def save_augmented_images(augmented_images, save_folder):
    """Salva as imagens aumentadas em uma pasta específica."""
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    for name, img in augmented_images:
        save_path = os.path.join(save_folder, name)
        cv2.imwrite(save_path, img)

def augment_faces(base_path, output_path, prefix="aug_"):
    """Percorre as subpastas, realiza data augmentation nas imagens e as salva."""
    # Definir o pipeline de augmentação
    augmenter = iaa.Sequential([
        iaa.Fliplr(0.5), # Flip horizontal (probabilidade de 50%)
        iaa.Affine(rotate=(-15, 15)), # Rotação aleatória entre -15 e 15 graus
        iaa.Affine(shear=(-10, 10)), # Shear entre -10 e 10 graus
        iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}), # Translação
        iaa.Multiply((0.8, 1.2)), # Ajuste de brilho
        iaa.GaussianBlur(sigma=(0, 1.0)) # Adicionar borrão
    ])
    
    # Iterar sobre as subpastas (1 a 35)
    for i in range(1, 36):
        subfolder = os.path.join(base_path, str(i))
        if not os.path.exists(subfolder):
            print(f"Subpasta {subfolder} não encontrada, pulando.")
            continue
        
        # Carregar imagens da subpasta
        images = load_images_from_folder(subfolder)
        if not images:
            print(f"Sem imagens na subpasta {subfolder}, pulando.")
            continue
        
        # Aplicar data augmentation com prefixo nos nomes das imagens
        augmented_images = augment_images(images, augmenter, prefix)
        
        # Salvar as imagens aumentadas em uma nova pasta
        save_folder = os.path.join(output_path, str(i))
        save_augmented_images(augmented_images, save_folder)
        print(f"Augmentation concluído para a subpasta {subfolder}.")

# Caminhos de entrada e saída
base_path = "/home/ddnm.ad/33718174820/projetos/teste/14360/"
output_path = "/home/ddnm.ad/33718174820/projetos/teste/14360/"

# Executar a função
augment_faces(base_path, output_path)
