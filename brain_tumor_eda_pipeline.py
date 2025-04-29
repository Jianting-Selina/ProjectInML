import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from tqdm import tqdm
import random
from PIL import Image
import matplotlib.gridspec as gridspec
from collections import Counter
import shutil

class DatasetExplorer(BaseEstimator, TransformerMixin):
    """
    Explores the structure of the brain tumor dataset and counts images per category
    """
    def __init__(self, base_path):
        self.base_path = base_path
        self.categories = None
        self.image_counts = None
        self.total_images = 0
        
    def fit(self, X=None, y=None):
        return self
    
    def transform(self, X=None):
        print("Exploring dataset structure...")
        
        # Get all categories (assuming they are subfolder names)
        self.categories = [cat for cat in os.listdir(self.base_path) 
                          if os.path.isdir(os.path.join(self.base_path, cat))]
        
        # Count images in each category
        self.image_counts = {}
        self.file_paths = []
        self.labels = []
        
        for category in self.categories:
            category_path = os.path.join(self.base_path, category)
            if os.path.isdir(category_path):
                files = [f for f in os.listdir(category_path) 
                         if f.endswith(('.jpg', '.jpeg', '.png', '.tif'))]
                
                self.image_counts[category] = len(files)
                self.total_images += len(files)
                
                # Store file paths and corresponding labels
                for file in files:
                    self.file_paths.append(os.path.join(category_path, file))
                    self.labels.append(category)
        
        print(f"Found {len(self.categories)} categories: {self.categories}")
        print(f"Total images: {self.total_images}")
        for category, count in self.image_counts.items():
            print(f"  - {category}: {count} images ({count/self.total_images*100:.1f}%)")
        
        # Create a dataframe with file paths and labels
        data = {
            'file_paths': self.file_paths,
            'labels': self.labels,
            'categories': self.categories,
            'image_counts': self.image_counts
        }
        
        return data


class ClassDistributionVisualizer(BaseEstimator, TransformerMixin):
    """
    Visualizes the class distribution in the dataset
    """
    def __init__(self, output_dir='./eda_results'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
    def fit(self, X=None, y=None):
        return self
    
    def transform(self, data):
        print("Visualizing class distribution...")
        
        # Plot class distribution
        plt.figure(figsize=(10, 6))
        plt.bar(data['image_counts'].keys(), data['image_counts'].values(), color='skyblue')
        plt.title('Class Distribution in Brain Tumor MRI Dataset')
        plt.xlabel('Classes')
        plt.ylabel('Number of Images')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot
        plot_path = os.path.join(self.output_dir, 'class_distribution.png')
        plt.savefig(plot_path)
        plt.close()
        
        # Create a pie chart for percentage distribution
        plt.figure(figsize=(8, 8))
        plt.pie(data['image_counts'].values(), labels=data['image_counts'].keys(), 
                autopct='%1.1f%%', startangle=90, shadow=True)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Percentage Distribution of Brain Tumor Classes')
        
        # Save the pie chart
        pie_chart_path = os.path.join(self.output_dir, 'class_percentage_distribution.png')
        plt.savefig(pie_chart_path)
        plt.close()
        
        print(f"Saved class distribution plots to {self.output_dir}")
        
        # Add visualization paths to data
        data['class_distribution_plot'] = plot_path
        data['class_percentage_plot'] = pie_chart_path
        
        return data


class ImageSampleVisualizer(BaseEstimator, TransformerMixin):
    """
    Visualizes sample images from each category
    """
    def __init__(self, samples_per_class=5, output_dir='./eda_results'):
        self.samples_per_class = samples_per_class
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
    def fit(self, X=None, y=None):
        return self
    
    def transform(self, data):
        print("Visualizing sample images from each class...")
        
        # Group file paths by label
        file_paths_by_label = {}
        for file_path, label in zip(data['file_paths'], data['labels']):
            if label not in file_paths_by_label:
                file_paths_by_label[label] = []
            file_paths_by_label[label].append(file_path)
        
        # Determine grid size based on number of classes and samples
        n_classes = len(data['categories'])
        n_samples = min(self.samples_per_class, 
                         min(len(paths) for paths in file_paths_by_label.values()))
        
        # Create a figure
        fig = plt.figure(figsize=(n_samples * 3, n_classes * 3))
        gs = gridspec.GridSpec(n_classes, n_samples)
        
        # Add images to the plot
        for i, category in enumerate(data['categories']):
            # Select random samples
            category_files = file_paths_by_label[category]
            if len(category_files) > n_samples:
                sampled_files = random.sample(category_files, n_samples)
            else:
                sampled_files = category_files
            
            # Plot each sample
            for j, file_path in enumerate(sampled_files):
                ax = plt.subplot(gs[i, j])
                try:
                    img = plt.imread(file_path)
                    ax.imshow(img, cmap='gray' if len(img.shape) == 2 else None)
                    ax.set_title(f"{category}" if j == 0 else "")
                    ax.axis('off')
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    ax.text(0.5, 0.5, f"Error loading image", 
                            ha='center', va='center')
                    ax.axis('off')
        
        plt.tight_layout()
        
        # Save the visualization
        samples_path = os.path.join(self.output_dir, 'sample_images.png')
        plt.savefig(samples_path, dpi=150)
        plt.close()
        
        print(f"Saved sample image visualization to {samples_path}")
        
        # Add visualization path to data
        data['sample_images_plot'] = samples_path
        
        return data


class ImageStatisticsAnalyzer(BaseEstimator, TransformerMixin):
    """
    Analyzes image statistics like dimensions, aspect ratios, and pixel intensity
    without using cv2
    """
    def __init__(self, sample_size=500, output_dir='./eda_results'):
        self.sample_size = sample_size
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
    def fit(self, X=None, y=None):
        return self
    
    def transform(self, data):
        print("Analyzing image statistics...")
        
        # If there are too many images, sample a subset
        if len(data['file_paths']) > self.sample_size:
            indices = random.sample(range(len(data['file_paths'])), self.sample_size)
            sampled_paths = [data['file_paths'][i] for i in indices]
            sampled_labels = [data['labels'][i] for i in indices]
        else:
            sampled_paths = data['file_paths']
            sampled_labels = data['labels']
        
        # Collect statistics
        statistics = []
        
        for file_path, label in tqdm(zip(sampled_paths, sampled_labels), 
                                     total=len(sampled_paths)):
            try:
                img = Image.open(file_path)
                img_array = np.array(img)
                
                # Convert to grayscale for analysis if it's RGB by averaging channels
                if len(img_array.shape) == 3:
                    if img_array.shape[2] == 3:  # RGB
                        gray_img = np.mean(img_array, axis=2).astype(np.uint8)
                    elif img_array.shape[2] == 4:  # RGBA
                        gray_img = np.mean(img_array[:,:,:3], axis=2).astype(np.uint8)
                    else:
                        gray_img = img_array[:,:,0]  # Take first channel
                else:
                    gray_img = img_array
                
                # Calculate statistics
                width, height = img.size
                aspect_ratio = width / height
                mean_intensity = np.mean(gray_img)
                std_intensity = np.std(gray_img)
                min_intensity = np.min(gray_img)
                max_intensity = np.max(gray_img)
                
                statistics.append({
                    'file_path': file_path,
                    'label': label,
                    'width': width,
                    'height': height,
                    'aspect_ratio': aspect_ratio,
                    'mean_intensity': mean_intensity,
                    'std_intensity': std_intensity,
                    'min_intensity': min_intensity,
                    'max_intensity': max_intensity
                })
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Convert to DataFrame
        stats_df = pd.DataFrame(statistics)
        
        # Save the statistics
        stats_path = os.path.join(self.output_dir, 'image_statistics.csv')
        stats_df.to_csv(stats_path, index=False)
        
        # Create visualization for dimensions
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        sns.scatterplot(data=stats_df, x='width', y='height', hue='label', alpha=0.7)
        plt.title('Image Dimensions by Class')
        plt.xlabel('Width (pixels)')
        plt.ylabel('Height (pixels)')
        
        plt.subplot(1, 2, 2)
        sns.histplot(data=stats_df, x='aspect_ratio', hue='label', bins=20, alpha=0.7)
        plt.title('Aspect Ratio Distribution by Class')
        plt.xlabel('Aspect Ratio (width/height)')
        
        plt.tight_layout()
        dims_path = os.path.join(self.output_dir, 'image_dimensions.png')
        plt.savefig(dims_path)
        plt.close()
        
        # Create visualization for intensity statistics
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 2, 1)
        sns.boxplot(data=stats_df, x='label', y='mean_intensity')
        plt.title('Mean Pixel Intensity by Class')
        plt.xticks(rotation=45)
        
        plt.subplot(2, 2, 2)
        sns.boxplot(data=stats_df, x='label', y='std_intensity')
        plt.title('Std Dev of Pixel Intensity by Class')
        plt.xticks(rotation=45)
        
        plt.subplot(2, 2, 3)
        sns.boxplot(data=stats_df, x='label', y='min_intensity')
        plt.title('Min Pixel Intensity by Class')
        plt.xticks(rotation=45)
        
        plt.subplot(2, 2, 4)
        sns.boxplot(data=stats_df, x='label', y='max_intensity')
        plt.title('Max Pixel Intensity by Class')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        intensity_path = os.path.join(self.output_dir, 'intensity_statistics.png')
        plt.savefig(intensity_path)
        plt.close()
        
        print(f"Saved image statistics to {stats_path}")
        print(f"Saved dimension plots to {dims_path}")
        print(f"Saved intensity plots to {intensity_path}")
        
        # Add statistics to data
        data['image_statistics'] = stats_df
        data['dims_plot_path'] = dims_path
        data['intensity_plot_path'] = intensity_path
        
        return data


def create_brain_tumor_eda_pipeline(dataset_path, output_dir='./eda_results'):
    """
    Create a sample EDA pipeline for the brain tumor MRI dataset
    
    Parameters:
    -----------
    dataset_path : str
        Path to the dataset directory containing class subfolders
    output_dir : str
        Directory where results will be saved
    
    Returns:
    --------
    Pipeline
        Scikit-learn pipeline for EDA
    """
    
    return Pipeline([
        ('explorer', DatasetExplorer(dataset_path)),
        ('class_visualizer', ClassDistributionVisualizer(output_dir)),
        ('sample_visualizer', ImageSampleVisualizer(samples_per_class=5, output_dir=output_dir)),
        ('statistics_analyzer', ImageStatisticsAnalyzer(sample_size=500, output_dir=output_dir))
    ])


# Example usage
if __name__ == "__main__":
    # Set paths
    dataset_path = '/path/to/brain-tumor-mri-dataset'
    output_dir = './brain_tumor_eda_results'
    
    # Create and run the pipeline
    pipeline = create_brain_tumor_eda_pipeline(
        dataset_path=dataset_path,
        output_dir=output_dir
    )
    
    # Execute the pipeline
    results = pipeline.fit_transform(None)
    
    print("EDA pipeline completed successfully!")
    print(f"Results saved to: {output_dir}")