IFRAME https://ieeexplore.ieee.org/document/11535283:
Opens in a new window Opens an external website Opens an external website in a new window
<!---->Close this consent banner<!---->
This website utilizes technologies such as cookies to enable essential site functionality, as well as for analytics, personalization, and targeted advertising. To learn more, view the following link:    [Privacy Policy](https://www.ieee.org/security-privacy.html)

Storage Preferences
   <!----><!---->
Skip to main content
Image Copyright Dual-Protection Based on Extractable and Imperceptible Adversarial Watermark | TUP Journals & Magazine | IEEE Xplore
Skip to Main Content
* [IEEE.org](https://www.ieee.org/)
* [IEEE *Xplore*](https://ieeexplore.ieee.org/Xplore/home.jsp)
* [IEEE SA](https://standards.ieee.org/)
* [IEEE Spectrum](https://spectrum.ieee.org/)
* [More Sites](https://www.ieee.org/sitemap.html)
[Subscribe](https://innovate.ieee.org/Xplore/Subscribebutton)
* [Donate](https://www.ieee.org/give)
* [Cart](https://www.ieee.org/cart/public/myCart/page.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE%20Xplore "View Cart")
* [Create Account](javascript:void() "Create Account")
* [Personal Sign In](javascript:void() "Sign In")
* Browse
* My Settings
* Help
[Institutional Sign In](javascript:void())
Institutional Sign In
Search by Content Type
AllBooksConferencesCoursesJournals & MagazinesStandardsAuthorsCitations
[ADVANCED SEARCH](https://ieeexplore.ieee.org/search/advanced)
Search by Content Type
AllBooksConferencesCoursesJournals & MagazinesStandardsAuthorsCitations
[ADVANCED SEARCH](https://ieeexplore.ieee.org/search/advanced)
[Journals & Magazines](https://ieeexplore.ieee.org/browse/periodicals/title/) >[Big Data Mining and Analytics](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8254253) >[Volume: 9 Issue: 3](https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=11535266&punumber=8254253)
# Image Copyright Dual-Protection Based on Extractable and Imperceptible Adversarial Watermark
Publisher: TUP
Cite This
[PDF](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11535283)
[Yuming Liu](https://ieeexplore.ieee.org/author/928425114552402); [Shan Ai](https://ieeexplore.ieee.org/author/37089286005); [Zhili Zhou](https://ieeexplore.ieee.org/author/37085877213); [Wei Pang](https://ieeexplore.ieee.org/author/37085446841); [Changyu Dong](https://ieeexplore.ieee.org/author/37086197391); [Huilin Ge](https://ieeexplore.ieee.org/author/37090089210)
[All Authors](javascript:void())
View Document
164
Full
Text Views
Open Access
* [Alerts](javascript:void())
  # Alerts
  [Manage Content Alerts](https://ieeexplore.ieee.org/alerts/citation)
  [Add to Citation Alerts](javascript:void())
---
[Abstract](https://ieeexplore.ieee.org/document/11535283)
## Document Sections
* [1
  Introduction](javascript:void())
* [2
  Related Work](javascript:void())
* [3
  Methodology](javascript:void())
* [4
  Experiment](javascript:void())
* [5
  Conclusion](javascript:void())
[Authors](https://ieeexplore.ieee.org/document/11535283/authors)
[Figures](https://ieeexplore.ieee.org/document/11535283/figures)
[References](https://ieeexplore.ieee.org/document/11535283/references)
[Keywords](https://ieeexplore.ieee.org/document/11535283/keywords)
[Metrics](https://ieeexplore.ieee.org/document/11535283/metrics)
[More Like This](https://ieeexplore.ieee.org/document/11535283/similar)
* [Download PDF](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11535283)
* [Download References](javascript:void())
* Request Permissions
* Save to
* Alerts
## Abstract:
Generally, there are two popular ways to protect image copyright, i.e., proactive protection (preventing illegal use via adversarial perturbation) and passive protection ...Show More
## Metadata
## Abstract:
Generally, there are two popular ways to protect image copyright, i.e., proactive protection (preventing illegal use via adversarial perturbation) and passive protection (verifying ownership by digital watermarking). However, since the perturbation and watermark embedded into an image will interfere with each other, directly embedding them into the image cannot achieve the proactive protection and passive protection, simultaneously. To address this issue, we propose an image copyright dual-protection approach, which embeds an Extractable and Imperceptible Adversarial Watermark (EIAW) in the image frequency-domain. Specifically, the adversarial watermark is automatically embedded and optimized in the manner of allowing for effectively attacking the Deep Neural Networks (DNNs) and accurately extracting the embedded watermark, simultaneously. Moreover, instead of using the pixel-domain constraints, i.e., Lp norms, we introduce a frequency-domain constraint to optimize the watermark embedding locations. Experiments on ImageNet and CIFAR-10 demonstrate that the proposed EIAW achieves high attack effectiveness (up to 100%) and extraction accuracy (up to 93%), while maintaining good watermark imperceptibility.
**Published in:** [Big Data Mining and Analytics](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8254253) ( Volume: 9, [Issue: 3](https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=11535266&punumber=8254253), June 2026)
**Page(s):**  719 - 734
**Date of Publication:** 26 May 2026
## ISSN Information:
**DOI:** [10.26599/BDMA.2025.9020070](https://doi.org/10.26599/BDMA.2025.9020070)
Publisher: TUP
## Funding Agency:
Contents
---
SECTION 1
## Introduction
With the widespread use of portable devices and online platforms, social media platforms, such as Facebook, Twitter, and Instagram, have become the main channels for sharing images. However, sharing extensive images comes with two main risks. First, user-uploaded images may be automatically recognized and analyzed by Deep Neural Networks (DNNs) to obtain sensitive semantic information, such as age and gender[[1]](javascript:void()); Second, images distributed on networks could be illegally copied for unauthorized use. Therefore, in the era of artificial intelligence, it is urgently required to protect the image copyright both before and after the illegal use of images. The image copyright dual-protection including the proactive protection (preventing the illegal use) and the passive protection (verifying image ownership after the illegal use) has become more and more important.
Generally, there are two popular ways to protect image copyright, i.e., adversarial attack and digital watermarking. The adversarial attack[[2]](javascript:void())–​[[5]](javascript:void()) usually adds an adversarial perturbation into a copyrighted image to mislead the model inference process, thereby preventing the illegal use of the image. However, such adversarial perturbations are added into images in an irreversible way and thus cannot be extracted accurately for verifying the image ownership. The digital watermarking[[6]](javascript:void())–​[[9]](javascript:void()) can embed a watermark into an image to verify ownership after unauthorized use. However, digital watermarking cannot prevent illegal use or copyright infringement in advance. To achieve copyright dual-protection, the most intuitive manner is to embed both a digital watermark and an adversarial perturbation into an image, sequentially. However, the embedded digital watermark and adversarial perturbation may affect each other, which makes the watermark difficult to be extracted and the adversarial perturbation ineffective. In addition, some adversarial watermarking approaches[[10]](javascript:void()), [[11]](javascript:void()) have been proposed, which embed a watermark as the adversarial perturbation into images. However, they often fail to enable accurate watermark extraction. Therefore, existing methods struggle to achieve effective dual-protection of image copyright.
To solve the above issues, in this paper, we propose a dual-protection approach for image copyright based on an Extractable and Imperceptible Adversarial Watermark (EIAW). Specifically, we design a strategy for embedding and optimizing the adversarial watermark using modulo operations in the frequency domain. It first generates and embeds a base adversarial watermark in the frequency embedding space, and then automatically optimizes it to attack DNNs within an embedding subspace without affecting the extractability of the watermark. As a result, this approach can effectively attack DNNs while allowing the embedded watermark to be accurately extracted. Additionally, unlike traditional methods that rely on $L\_{p}$ norms for optimizing the adversarial watermark in the pixel domain[[3]](javascript:void())–​[[5]](javascript:void()), which has been proven to poorly align with human perception[[12]](javascript:void()). We introduce a frequency domain constraint to optimize watermark embedding locations, which ensures the final watermarked images maintain high quality. We illustrate the differences among the adversarial attack, digital watermark, and the proposed EIAW in Fig. 1.
In summary, our main contributions are summarized as follows:
* **EIAW is proposed for image copyright dual-protection**: Unlike existing adversarial attack or digital watermark methods, EIAW allows for effectively attacking DNNs and accurately extracting the watermark, enabling image copyright dual-protection.
* **Frequency domain constraint is designed to optimize the imperceptibility of the adversarial watermark**: Instead of using $L\_{p}$ norms to limit the perturbation in the pixel domain, we introduce a frequency domain constraint to optimize the watermark embedding locations, achieving more imperceptible adversarial watermarked images.
* **Superiority of the proposed approach is proven by extensive experiments**: Extensive experiments show that the proposed EIAW method not only achieves comparable attack effectiveness and efficiency to state-of-the-art methods, i.e., PGD, but also maintains high watermark imperceptibility, accurate watermark extraction, and robustness against various noise attacks.
The structure of this paper is organized as follows.
**Fig. 1**
Comparison of different approaches. (a) Proactive protection via adversarial attack is able to prevent illegal use, (b) passive protection via digital watermark is able to verify ownership, and (c) our dual-protection approach based on EIAW can prevent illegal use and verify ownership, simultaneously.
Show All
Section 2 discusses the related work. Section 3 describes the proposed EIAW method in detail. Section 4 presents and analyzes the experimental results. Section 5 concludes the paper.
SECTION 2
## Related Work
In this section, we review relevant works in three areas: adversarial attack, digital watermarking, and adversarial watermark attacks.
### 2.1 Adversarial Attack
Adversarial attack deceives DNNs by adding small perturbations to images. These perturbations can alter the model's predictions, preventing DNNs from accurately analyzing the image and thus protecting the image's semantic information. Early research by Szegedy et al.[[2]](javascript:void()) introduced adversarial perturbations using back-propagation and gradient-based algorithms. Since then, various methods have been proposed to generate adversarial examples[3-5,13,14]. A well-known gradient-based method is the Fast Gradient Sign Method (FGSM)[[5]](javascript:void()), which crafts perturbations by taking a step in the direction of the gradient. Similarly, the Projected Gradient Descent (PGD) attack[[3]](javascript:void()), often considered state-of-the-art, updates perturbations iteratively starting from random initialization.
The above methods are usually carried out in the pixel domain, recent research has also explored adversarial attacks in the frequency domain. For example, Wang et al.[[15]](javascript:void()) demonstrated the sensitivity of DNNs to high-frequency components, leading to the development of frequency domain adversarial attacks. Luo et al.[[16]](javascript:void()) proposed a method that enhances imperceptibility by minimizing differences between the low-frequency components of clean and adversarial images. S2I-FGSM[[17]](javascript:void()) enhances transferability through spectrum transformations in the frequency domain. AdvDrop[[18]](javascript:void()) takes a unique approach by crafting adversarial examples through information removal rather than addition, demonstrating that minimal frequency component manipulation can significantly impact model performance. While Guo et al.[[19]](javascript:void()) constrained perturbations to specific frequency bands to reduce the number of black-box queries, our work focuses on optimizing perturbations in these bands to improve both attack effectiveness and watermark imperceptibility.
Despite these advancements, $L\_{p}$ norms are commonly used to constrain perturbations for generating more imperceptible adversarial examples. However, recent studies show that $L\_{p}$ norms do not align well with human perception[[12]](javascript:void()). Therefore, other perceptual distances, such as Structural Similarity Index Measure (SSIM)[[20]](javascript:void()) and Learned Perceptual Image Patch Similarity (LPIPS)[[21]](javascript:void()), have been used to improve imperceptibility. Inspired by this, our work introduces a frequency domain constraint to generate perturbations that are less perceptible to human vision, achieving highly imperceptible adversarial watermarks.
### 2.2 Digital Watermarking
Digital watermarking embeds meaningful information, such as copyright ownership, content description into digital content. It provides an effective solution for copyright protection, and is widely used to track and prevent copyright infringement[6,22–24].
In general, digital watermarks can be classified into visible and invisible watermarks based on their visual effects. Visible watermarks[[7]](javascript:void()) are more perceptible to human eyes, making them more susceptible to targeted attacks and modifications. In contrast, invisible watermarks[8,9,25] use data redundancy techniques that typically bypass the human visual system. Recent advances in invisible watermarking have focused on enhancing robustness against complex distortions. For instance, Li et al.[[26]](javascript:void()) proposed a grayscale deviation simulation method to resist screen-shooting distortions, while Fu et al.[[27]](javascript:void()) developed a wavelet-based recovery network to maintain watermark integrity under various image processing operations. These works demonstrate the importance of domain-specific transformations for robust watermarking, which aligns with our frequency domain approach. Furthermore, Liao et al.[[28]](javascript:void()) showed that robust feature extraction in compressed media can effectively preserve critical information, further supporting our choice of frequency domain embedding for adversarial watermarking. Additionally, depending on whether the original image is required for extraction, watermarking methods are classified as blind or non-blind. Non-blind methods merge the original and watermark images, requiring the original image during extraction. Blind watermarking embeds watermarks directly using specific rules, allowing extraction without the original image. In this work, we employ an invisible, blind-extractable watermark in the frequency domain to craft adversarial watermarks.
### 2.3 Adversarial Watermark Attacks
Recent studies have explored using watermarks as adversarial perturbations to attack DNNs. Jia et al.[[10]](javascript:void()) proposed the Basin Hopping Evolution (BHE) algorithm to embed visible watermarks into images, causing inference errors in DNNs. Jiang et al.[[29]](javascript:void()) improved this with a fast differential evolution method. Zuo et al.[[30]](javascript:void()) enhanced the Multi-swarm Particle Swarm Optimization (MPSO) algorithm to conduct extensive attack experiments. However, all above methods add watermarks in the pixel domain and use visible watermarks to attack. It is clear that visible watermarks degrade the quality of the protected images and are easy to notice. To generate more imperceptible images, Zhang et al.[[11]](javascript:void()) introduced a frequency domain adversarial watermarking framework, which embeds adversarial watermarks in the frequency coefficients. Although this watermark is invisible, they still need the original image for extraction, limiting its practical use.
Some studies have used adversarial watermarks to protect image copyright. For example, Zhu et al.[[31]](javascript:void()) proposed adversarial examples with embedded watermarks to stop generative models from copying unauthorized images. Wang et al.[[32]](javascript:void()) designed an end-to-end Adversarial Watermark Fusion Model (AWFM) that combines watermark embedding and adversarial perturbations into a single task to generate invisible adversarial watermarked images. However, training these models is challenging because they require optimizing multiple objectives simultaneously.
In this paper, we propose a dual-protection adversarial watermarking framework. It embeds extractable watermarks into the frequency coefficients under the constraints, ensuring imperceptibility while enabling watermarks can be extracted accurately.
SECTION 3
## Methodology
### 3.1 Overview
Given an original watermark image $W\_{\text{in}}\in \mathbf{R}^{N\times N}$, a cover image $I\in \mathbf{R}^{N\times N}$, its ground-truth label $y$, and a DNN classifier $f;I\rightarrow \mathbf{R}^{k}$ that maps the image to an output vector representing a probability distribution over the discrete label set $\{1, 2, \ldots, k\}$, where $k$ is the number of classes. We use the cross-entropy as the loss function, denoted by *L*. The formula for the cross-entropy loss is
\begin{equation\*}
L=-\sum\_{i=1}^{k}y\_{i}\log(f(I)\_{i}),\end{equation\*}View Sourcewhere $y\_{i}$ is the ground-truth label for class $i$, and $f(I)\_{i}$ is the predicted probability for class $i$.
Let $I\_{\text{adv}}$ denote the adversarial example, $I\_{\mathrm{w}}$ denote the watermarked image after embedding the base watermark, $W\_{\text{out}}$ denote the extracted watermark, $F$ represent the frequency domain coefficient matrix of the cover image, $F\_{\mathrm{w}}$ denote the frequency-domain matrix after watermark embedding, and $F\_{\text{aw}}$ denote the adversarial frequency domain matrix generated during the attack process. We use the Discrete Cosine Transform (DCT) to convert the cover image from the pixel domain to the frequency domain, and employ the Inverse DCT (IDCT) to revert it back.
The goal of adversarial attacks is to craft $I\_{\text{adv}}$ such that $f(I\_{\text{adv}})\neq y$, while the aim of blind watermarking is to embed a watermark $W\_{\text{in}}$ into the cover image to obtain the watermarked image $I\_{\mathrm{w}}$, from which the watermark information $W\_{\text{out}}$ can be extracted accurately. Different from the above two methods, our goal is to embed and optimize a watermark into the image $I$ while allowing for effectively attacking DNNs and accurately extracting the watermark, simultaneously. In this paper, we propose a novel frequency domain adversarial watermark algorithm EIAW, which can generate extractable and imperceptible adversarial watermark. The pipeline of the EIAW approach is shown in Fig. 2.
Next, we will first introduce the frequency domain constraint, followed by a detailed presentation of our proposed EIAW, approach by three parts: watermark embedding, watermark optimization, and watermark extraction.
### 3.2 Frequency Domain Constraint
In digital watermarking, watermarks are often embedded in the frequency domain. This approach inspires us to craft watermark perturbations directly in the frequency domain. To evaluate the effectiveness of perturbations in different frequency regions, we calculate the gradients of the loss function $L$ with respect to both the frequency domain image $F$ and the pixel domain image *I*,
\begin{gather\*}\nabla\_{F} L=\frac{\partial L(\theta, \text{IDCT}\ (F), y)}{\partial I} \cdot \frac{\partial I}{\partial F}\tag{1}\\
\nabla\_{I} L=\frac{\partial L(\theta, I, y)}{\partial I}\tag{2}\end{gather\*}View Sourcewhere $\theta$ represents the model parameters, $\nabla\_{F}L$ and $\nabla\_{I}L$ are the gradients of the loss function $L$ with respect to the input image $F$ (in the frequency domain) and the image $I$ (in the pixel domain), respectively, and $y$ is the true label of the cover image.
**Fig. 2**
Pipeline of the proposed EIAW approach. Operator ⊕ denotes a additive update that applies a masked signed-gradient perturbation to the watermarked image.
Show All
The magnitude of these gradients indicates how changes at each location affect the loss. In other words, regions with larger gradients have a greater influence on the model's inference.
To make it more intuitive, we visualize the gradient heatmaps in Fig. 3. From the heatmaps, we observe that the gradient distribution in the pixel domain lacks distinct patterns. In contrast, the frequency domain gradient distribution shows a clear trend. Specifically, mid-to-low frequency regions (top-left in each subfigure in Fig. 3) exhibit larger gradients, while high-frequency regions (bottom-right in each subfigure in Fig. 3) have smaller gradients. This means that perturbations in mid-to-low frequency regions achieve better attack performance. Even small perturbations in these regions can significantly affect the model's predictions. Although these perturbations may cause some degradation in image quality, the improved attack effectiveness outweighs the visual loss. Overall, disturbances in low and medium frequencies are more cost-effective.
**Fig. 3**
Gradient heatmaps of the RGB channel in the frequency domain (a)-(c) and pixel domain (d)-(f). In the pixel domain, the axes X and Y denote the spatial coordinates of the image. In the frequency domain, the axes U and V denote the horizontal and vertical frequency coordinates obtained after applying the DCT, respectively.
Show All
Based on this observation, we design a frequency domain constraint to limit watermark perturbations to mid-to-low frequency regions. Specifically, we assign the value “1” to locations within the mid-to-low frequency areas, allowing perturbations to be added. All other regions are assigned the value “0”, creating a binary mask *M*,
\begin{equation\*}
M= \begin{cases}
1, & \text { if } m \leqslant u, v \leqslant n \\
0, & \text {otherwise}\end{cases}\end{equation\*}View Sourcewhere $m,\ n\in[0,\ N]$, and $N$ represents the dimension of the frequency-domain coefficient matrix $F$, equivalently, is the dimension of the pixel domain image $I.\ u$ and $v$ denote the horizontal and vertical coordinates in the frequency domain, respectively. The size of the mask is denoted as $\alpha=(n-m)/N\in[0,1]$, while the starting position of the mask is defined as $\beta=m/N$. For images with multiple color channels, the same masking strategy is applied independently to each channel.
During the watermark embedding and optimization stages, we only modify the DCT coefficients in regions where the mask value is 1. This ensures that the watermark perturbations are confined to the mid-to-low frequency areas.
### 3.3 Watermark Embedding
To enable accurate watermark extraction without requiring the cover image, we introduce the watermark embedding and extracting strategy based on modulo operation in the frequency domain. First, the image is transformed from the pixel domain to the frequency domain, where watermark bits are embedded by adjusting frequency coefficients based on the remainder of the modulo operation. More details are given as follows.
Within the masked region, where the watermark bit $w\_{\text{in}}=1$, the DCT coefficients are modified according to the strategy in Eq. [(3)](https://ieeexplore.ieee.org/document/11535283#deqn3):
\begin{align\*}
&\text {if}\ F(u, v)\ \text{mod}\ p \geqslant \frac{p}{2},\\
&\text {then}\ F(u, v) \longleftarrow F(u, v)+\frac{p}{2},\\
&\text {else}\ F(u, v) \longleftarrow F(u, v)\tag{3}\end{align\*}View Source
Conversely, when the watermark bit $w\_{\text{in}}=0$, we perform the strategy in Eq. [(4)](https://ieeexplore.ieee.org/document/11535283#deqn4):
\begin{align\*}
&\text {if}\ F(u, v)\ \text{mod}\ p < \frac{p}{2},\\
&\text {then}\ F(u, v) \longleftarrow F(u, v)+\frac{p}{2},\\
&\text {else}\ F(u, v) \longleftarrow F(u, v)\tag{4}\end{align\*}View Source
$F=\text{DCT}\ (I)$ represents the frequency-domain coefficient matrix obtained by applying the DCT to image $I$. The entry at position $(u,\ v)$ is written as $F(u,\ v)$. The parameter $p$ is the embedding key, which must be an even integer.
By modifying the DCT coefficients according to the above embedding strategy, we successfully embed the watermark and obtain the base watermarked image $I\_{\mathrm{w}}$. The embedding process is described in Algorithm 1. Notably, since explicit for-loops are computationally inefficient, we leverage PyTorch's array slicing operations to achieve implicit parallel computation, accelerating the watermark embedding.
### 3.4 Watermark Optimization
To obtain the adversarial watermark without affecting the watermark extraction, we optimize the watermark by changing the modification magnitudes of frequency coefficients to attack DNNs within the embedding subspace. In such manner, the remainders of DCT coefficients when divided by $p$ can be kept unchanged, and thus the extractability will not be affected. Specifically, to optimize the watermark in the frequency domain embedding subspace, we propagate the gradient of the loss using the following chain rule in Eq. [(1)](https://ieeexplore.ieee.org/document/11535283#deqn1-deqn2). Then, we update the DCT coefficients by stepping in the direction of the gradient. To avoid affecting the extractability of the watermark, the remainders of the DCT coefficients should remain unchanged. Therefore, the step size must be an integer multiple of $p$. The specific formula is as Eq. [(5)](https://ieeexplore.ieee.org/document/11535283#deqn5):
### Algorithm 1 EIAW Embedding Process
**Input**: Cover image *I*, watermark $w\_{\text{in}}$, modulus $p$, and mask $M$
**Output**: Watermarked image $I\_{\mathrm{w}}$
1:
$F=\text{DCT}\ (I)$;
2:
**for**$(u,\ v)$ in the mask region, $M=1$ **do**
3:
**if**$w\_{\text{in}}(u,\ v)=1$**then**
4:
if $F(u,\ v)$ mod $p\geqslant p/2$ **then**
5:
$F(u,\ v)\leftarrow F(u,\ v)+p/2;$
6:
**end if**
7:
**else**
8:
if $F(u,\ v)$ mod $p < p/2$ **then**
9:
$F(u,\ v)\leftarrow F(u,\ v)+p/2;$
10:
**end if**
11:
**end if**
12:
**end for**
13:
$I\_{w}=\text{IDCT}\ (F)$;
14:
**return**$I\_{w}$
\begin{equation\*}
F\_{\text{aw}}^{t+1}=F\_{\text{aw}}^{t}+p\times \text{sgn}(\nabla\_{F}L)\times M\tag{5}\end{equation\*}View Sourcewhere $\text{sgn} (\cdot)$ is the sign function, $M$ represents the frequency-domain mask. $F\_{\text{aw}}^{t}$ and $F\_{\text{aw}}^{t+1}$ denote the adversarial frequency-domain coefficient matrices at the *t-th* and *(t+* l)-th iteration, respectively.
Assuming the attack succeeds after $t+1$ iterations, $F\_{\text{aw}}=F\_{\text{aw}}^{t+1}$ denotes the frequency domain adversarial watermarked image. Then, we convert it back to the pixel domain to obtain the final image $I\_{\text{aw}}$,
\begin{equation\*}
I\_{\text{aw}}=\text{Clip}(\text{IDCT}(F\_{\text{aw}}), 0,1)\tag{6}\end{equation\*}View Sourcewhere $\text{Clip}\ (\cdot)$ is the operation that restricts the resulting values to the range [0, 1]. Algorithm 2 describes the pseudocode of optimization algorithm. By optimizing the watermark to attack DNNs within a frequency domain embedding subspace without affecting the extractability of the watermark, we achieve the dual goals of preventing illegal use and verifying ownership, simultaneously. To provide a clear visualization of the constrained optimization process, we illustrate the optimization process in Fig. 4.
### Algorithm 2 EIAW Optimization Process
**Input**: Classifier $f$ with loss function *L*, cover image *I*, label $I$, watermark $W\_{\text{in}}$, and key $p$
**Output**: Adversarial watermarked image $I\_{\text{aw}}$
1:
*F* = DCT(I);
2:
$F\_{\mathrm{w}}$ = Embed $(F,\ W\_{\text{in}},\ p,\ M)$;
3:
Initialize: iter ← 0, attack\_successful ← false;
4:
**while** iter $\leqslant$ Max\_iter **do**
5:
iter ← iter + 1;
6:
$F\_{\mathrm{w}}\leftarrow F\_{\mathrm{w}}+p\times\text{sgn}(\nabla\_{F\_{\mathrm{w}}}L)\times M$;
7:
$I\_{\text{aw}}\leftarrow\text{IDCT}\ (F\_{\mathrm{w}})$;
8:
**if**$\arg\max\_{\hat{y}}f(I\_{\text{aw}})\neq y)$**then**
9:
attack\_successful ← true;
10:
**break;**
11:
**end if**
12:
**end while**
13:
if attack successful **then**
14:
**return**$I\_{\text{aw}}$;
15:
**else**
16:
**return false;**
17:
**end if**
**Fig. 4**
**Visualization of the watermark optimization process. The**$X$**and $Y$ axes in the 2D space represent the modification magnitudes of DCT coefficients, i.e**., $\Delta F\_{1}$ and $\Delta F\_{2}$, **respectively. The 2D space represents the embedding space, and the set of green points in the 2D space represents the embedding subspace in which the adversarial watermark can be optimized without affecting its extractability**.
Show All
### 3.5 Watermark Extraction
Watermark extraction is the inverse process of embedding. Specifically, given the adversarial watermarked image $I\_{\text{aw}}^{\prime}$, we first convert it to frequency domain, then, in the region where. $M=1$, the watermark is extracted using the following strategy:
\begin{equation\*}
W\_{\text {out}}= \begin{cases}
1, & \text { if } \sum\limits\_{0}^{c-1}\left((F\_{\text {aw}}^{\prime}\ \text{mod} p) < \frac{p}{2}\right) \geqslant\lceil\frac{c}{2}\rceil \\
0, & \text {otherwise}\end{cases}\tag{7}\end{equation\*}View Sourcewhere $F\_{\text{aw}}^{\prime}=\text{DCT}\ (I\_{\text{aw}}^{\prime})$ denotes the DCT matrix, and $c$ denotes the number of pixel channels, with $c=3$ for **RGB** images. Finally, $W\_{\text{out}}$ is extracted to recover the original watermark $W\_{\text{in}}$ without the cover image.
Notably, in addition to embedding 2D binary watermark images, our method also supports direct embedding of arbitrary-length bit-streams. To achieve this, we employs Zigzag scanning[[33]](javascript:void()) to convert DCT coefficients into a 1D sequence. The bit-stream is then directly embedded into a selected mid-low frequency band whose length matches that of the bit-stream, enabling flexible and scalable embedding. The embedding, optimization, and extraction procedures for bit-streams follow the same strategy as those used for image-based watermarks, ensuring consistency and robustness.
SECTION 4
## Experiment
In this section, we evaluate and compare the proposed approach to demonstrate its performances in terms of attack effectiveness, efficiency, watermark extraction, and imperceptibility. Typical experimental results of EIAW approach are shown in Fig. 5. The original images can be correctly classified by ResNet101. After embedding the adversarial watermarks generated by EIAW, they can mislead the pretrained ResNet101 while maintaining good visual quality.
### 4.1 Experiment Setting
#### 4.1.1 Dataset and Model
We evaluate the proposed EIAW approach on 1500 images from the ImageNet-1K[[34]](javascript:void()) and CIFAR-10 datasets. We use ResNet101[[35]](javascript:void()), AlexNet[[36]](javascript:void()), VGG19[[37]](javascript:void()), SqueezeNetl\_0[[38]](javascript:void()), MobileNet\_ V2[39], and Inception\_V3[[40]](javascript:void()) as the target models.
#### 4.1.2 Baseline
To compare the effectiveness and efficiency of the watermark attack, we use several adversarial watermark attack methods: Adv-watermark[[10]](javascript:void()), AFW[[11]](javascript:void()), and MISPSO[[30]](javascript:void()). We also compare with typical gradient-based attack methods under the *Lp* norms, including PGD[[3]](javascript:void()), FGSM[[5]](javascript:void()), and C&W[[4]](javascript:void()). Additionally, we compare with the two-phase method that adds perturbations and watermarks sequentially.
#### 4.1.3 Evaluation Metric
We use the following metrics to evaluate the attack capability, extraction accuracy, and imperceptibility of different methods.
1. **Attack capability**: Attack effectiveness and efficiency are evaluated using the Attack Success Rate (ASR) and Attack Time (AT), respectively. ASR measures the percentage of images for which the pretrained model changes its prediction after the images are altered. AT measures the average time required to attack a single image. In addition, we also report the increase in cross-entropy loss (LOSS), where a larger LOSS indicates a greater degradation of model prediction accuracy, thus reflecting a more successful attack.
2. **Imperceptibility**: To sufficiently evaluate the watermark's imperceptibility, we use the Peak Signal-to-Noise Ratio (PSNR), SSIM[[20]](javascript:void()), and LPIPS[[21]](javascript:void()). These metrics compare the quality of the watermarked image with the original image to assess how perceptible the watermark.
3. **Extraction accuracy**: The Extraction Accuracy Rate (EAR) measures the watermark's extractability. It is calculated as the ratio of the number of correctly extracted bits to the total number of bits. A higher EAR value, closer to 1, indicates more accurate extraction.
#### 4.1.4 Evaluation Environment
To make a fair comparsion, all experiments are conducted on an NVIDIA GeForce RTX 3090 GPU using the PyTorch framework in Python.
**Fig. 5**
Experimental results of the EIAW method. The first row shows the original images, the second row displays the corresponding true labels, the third row presents the protected images generated by EIAW, along with their predicted labels, PSNR and SSIM metrics, and the last row shows the extracted watermark images.
Show All
### 4.2 Parameter Setting
In the proposed EIAW method, there are two key parameters: $p$, which is the key to conducted modular operation, and *M*, which determines where the watermark perturbation is applied. We evaluate the impact of these parameters on the method's performance in terms of attack capability and imperceptibility. The impacts of parameter $p$ is shown in Table 1. As it illustrates, increasing $p$ slightly improves attack efficiency by reducing the attack time. However, this improvement comes at huge cost of image quality, as evidenced by the decrease in PSNR and SSIM and the increase in **LPIPS** as $p$ grows. Therefore, we choose the smallest parameter $p=2$ to minimize quality loss.
The impact of the mask's location is shown in Fig. 6. Masks of the same size are applied to different frequency regions: low-frequency (M1), mid-low-frequency (M2), mid-high-frequency (M3), and high-frequency (M4). The plots show how the loss and image quality metrics change over iterations. From Fig. 6, it is clear that low-frequency perturbations are more effective for attacks, as they cause the loss to increase rapidly. However, they also significantly degrade image quality. On the other hand, high-frequency perturbations have a smaller impact on image quality but are less effective for attacks. Therefore, we constrain the perturbations to the mid-low-frequency region, which strikes a balance between attack effectiveness and image quality.
**Table 1** Impact of key p on attack time and watermark imperceptibility. “↑” means larger is better, while “↓” means smaller is better.
Finally, if not specified, the watermark attack parameters in EIAW are set as follows: $p=2,\ \alpha=0,\ \beta=0.5$, with a maximum of 20 iterations. Additionally, a monitoring mechanism is used for all iterative attack methods: if the attack is successful, the iteration terminates early.
### 4.3 Comparison of Attacking Performance
By embedding an additional watermark into the original image, we disrupt key local regions that are essential for image classification, effectively misleading a well-trained neural network. To illustrate the impact of the adversarial watermark, we visualize the attention maps using Gradient weighted Class Activation Mapping (Grad-CAM)[[41]](javascript:void()). As shown in Fig. 7, the clean images, correctly classified by ResNet101, along with their attention maps and labels in green (Fig. 7a). The adversarial watermarked images, along with their attention maps and labels in red (Fig. 7b), by embedding an additional watermark into the original image, we disrupt key local regions that are essential for classification, thereby misleading the well-trained Resnet101[[35]](javascript:void()) model.
To further quantitatively evaluate the attack performance of the proposed EIAW method, we compare six attack methods across five widely used pretrained classification models (ResNet101, AlexNet, VGG19, Inception\_V3, and SqueezeNet1\_0) on ImageNet-1K[[34]](javascript:void()) and CIFAR-10 datasets. Table 2 shows the Attack Success Rates (ASR) of various attack methods on different neural network models. Traditional attack methods, such as PGD[[3]](javascript:void()) and C&W[[4]](javascript:void()), achieve high ASRs across all models. The Adv-watermark method[[10]](javascript:void()), based on visible watermarking, achieves an average ASR of 71.7%, while the MISPSO[[30]](javascript:void()) method, using the MPSO algorithm, reaches 75.9%. The AFW method, which embeds the watermark in the frequency domain, achieves a high ASR of 97.4%. In comparison, our proposed EIAW method achieves a comparable attack effectiveness to PGD[[3]](javascript:void()), and outperforms other adversarial watermark methods. We further evaluate the black-box transferability of EIAW through comprehensive cross-model validation. As shown in Table 3, when adversarial examples generated from one model architecture are transferred to attack other unseen models, these results demonstrate that our frequency domain perturbations maintain reasonable effectiveness across different architectures, making them practical for real-world scenarios where the target model may be unknown.
**Fig. 6**
Impact of the frequency domain mask's location on image quality, showing the mask applied to different regions (M1, M2, M3, and M4) and illustrating the changes in LOSS, SSIM, and LPIPS across iterations.
Show All
**Fig. 7**
Effects of EIAW on the attention maps of neural networks (based on ResNet101 predictions). (a) Original image and the corresponding attention map, where the model makes correct predictions. (b) Adversarially watermarked image and the corresponding attention map, where EIAW disrupts the model's attention distribution, leading to incorrect predictions.
Show All
Next, we evaluate the efficiency of the proposed method. Table 4 compares the attack efficiency of the EIAW method with the state-of-the-art PGD[[3]](javascript:void()) attack and the adversarial watermark method AFW. As shown in Table 4, EIAW achieves an average ASR of 99.6% with a runtime of 0.0467 s. This is slightly slower than PGD, but much faster than AFW. This shows that, despite the conversions between the frequency domain and pixel domain, the additional computational cost is minimal. However, this minor time overhead provides significant benefits, such as improved image quality and the ability to extract the watermark for dual protection, as demonstrated in the following sections.
### 4.4 Comparison of Imperceptibility
To achieve a more secure and practical copyright protection, the protected image should be visually indistinguishable from the original image. In this section, we compare the imperceptibility of watermarks or perturbations generated by different methods. To sufficiently evaluate the imperceptibility, we use three standard metrics: PSNR, SSIM[[20]](javascript:void()), and LPIPS[[21]](javascript:void()). Higher PSNR and SSIM values indicate better image quality, while lower LPIPS values reflect less perceptual distortion, meaning the watermark or perturbation is less noticeable to the human eye.
**Table 2** ASR comparison with various methods on ImageNet-1K against different models. Bold value indicates the best result in each column.
**Table 3** Transferability of ASR for adversarial watermarked images across surrogate and attack models. Bold value indicates the best result in each column.
**Table 4** Comparison of ASR and AT across different models and attack methods on Image Net-1K and CIFAR-10 datasets.
As shown in Table 5, for the ResNet101 model, EIAW achieves the highest PSNR of 52.68 and SSIM of 0.9970, outperforming other methods. Its LPIPS score of 0.0006 indicates that the perceptual difference between the original and protected images is minimal. Similar results are observed for other models, where EIAW consistently achieves higher PSNR and SSIM values and lower LPIPS scores compared to other methods. In comparison, attack methods such as PGD[[3]](javascript:void()) and FGSM[[5]](javascript:void()), which constrain perturbation in the pixel domain using $L\_{p}$ norms, cause significant quality degradation. Other adversarial watermark methods, such as Adv-watermark, embed visible watermarks, making them more noticeable and leading to greater quality loss. Although AFW operates in the frequency domain, it applies perturbations to the entire coefficient, resulting in noticeable distortions as well. In contrast, our method uses a frequency domain constraint to limit perturbations to specific regions, achieving better image quality.
**Table 5** Comparison of imperceptibility against different models under various attack methods on ImageNet-1K. Bold value indicates the best result in each column. “↑” means larger is better, while “↓” means smaller is better.
### 4.5 Watermark Extraction Performance
In this section, we evaluate the watermark extraction performance of the proposed method. From Table 6, we can see that EIAW achieves a high watermark EAR of over 91% across different models. This level of performance is sufficient for practical applications, such as copyright verification. We do not compare our method with Adv-watermark and AFW here, as both require the original image for watermark extraction, while our approach can extract the watermark based solely on the secret key $p$, which is more suitable for real-world applications.
**Table 6** Average EAR of EIAW on different models. Bold value indicates the best result.
The watermark should remain extractable even when the image is distorted by various attacks. Therefore, to further demonstrate the robustness of the watermark extraction, we conduct both qualitative and quantitative evidence of the watermark's resilience to common image processing operations. As shown in Fig. 8 and Table 7, we apply several common image distortions, such as JPEG compression, and cropping, and evaluate the watermark extraction performance under these conditions. The results show that, although the extracted watermark images exhibit some distortion after noise is added, the watermark remains recognizable. This demonstrates that our method can preserve copyright information even under distortions.
### 4.6 Bit-Stream Embedding Evaluation
To further validate the flexibility and effectiveness of our method, we conduct an additional experiment using bit-stream embedding instead of binary watermark images. Specifically, we adopt a Zigzag-based encoding[[33]](javascript:void()) strategy to directly embed arbitrary-length bit-streams into the mid-low frequency band of the DCT domain, the length of this band is the same as the length of the bit-stream. The experimental results are presented in Table 8. Across different bit-stream lengths (512 bits to 4096 bits), the proposed method consistently achieves high PSNR values, indicating excellent imperceptibility. Notably, the watermark extraction remains robust, with EAR improving as the bit length increases, reaching 93.6% in the 4096-bit case. Similarly, the ASR increases with the embedding payload, achieving 100% when embedding 4096 bits.
From a theoretical perspective, our method modifies DCT coefficients through constrained optimization, which is agnostic to the semantic content of the embedded data. Whether the watermark is a 2D binary image or a 1D bit-stream, they are mathematically isomorphic in the frequency domain. Moreover, the energy distribution in the selected frequency band remains consistent across different input formats, which ensures that the embedding process is format-independent. These demonstrate that our method not only supports 2D binary watermark images, but also generalizes well to arbitrary bit-streams, further extending its applicability to real-world digital copyright protection.
### 4.7 Comparison with Two-Phase Method
To achieve copyright dual-protection, the most intuitive manner is to embed the watermark and perturbation sequentially, which we denote as the two-phase method. To demonstrate the superiority of our method over the two-phase approach, we conducted experiments in terms of the ASR, EAR, and imperceptibility.
The results are shown in Table 9, as we can see, in terms of EAR, the proposed EIAW method achieves an extraction accuracy of 92.34%, outperforming the two-phase method. This is mainly because, when the perturbation and watermark are added sequentially, they interfere with each other, making extraction more difficult. And in terms of imperceptibility, because the two-phase method requires two modifications, it leads to greater quality degradation. In contrast, EIAW embeds a single adversarial watermark and improves image quality using a frequency domain constraint, thereby achieving better performance.
**Fig. 8**
Robustness of the watermark under different noises. (a) Protected images with different editing operations, and (b) extracted watermark images.
Show All
**Table 7** Robustness of watermark EAR and ASR on ImageNet-1K. “-” denotes the identity setting (no-attack), where the watermarked images are evaluated without any distortion.
**Table 8** Bit-stream embedding performance.
### 4.8 Ablation Study
In this section, we conduct an ablation study to prove the effect of the frequency domain constraint on image quality. We compare three strategies: (1) frequency domain constrained attack (namely F-c), which applies perturbations to specific frequency components using the mask, (2) frequency domain full coverage attack (namely F-f), which applies perturbations to all frequency components, and [(3)](https://ieeexplore.ieee.org/document/11535283#deqn3) pixel domain full coverage attack (namely P-f), which applies perturbations to the entire image in the pixel domain, and using $L\_{p}$ norms to constrain the perturbations.
As shown in Fig. 9, the F-c achieves the best image quality among the three strategies. In contrast, the F-f, which applies perturbations to all frequencies, causes more image quality degradation, even worse than the P-f. It further validates the effectiveness of our frequency domain constraint in improving image quality.
SECTION 5
## Conclusion
This paper introduces a novel approach for dual-protection of image copyright, based on an extractable and imperceptible adversarial watermark, EIAW. It automatically embeds and optimizes an adversarial watermark to prevent illegal use and verify ownership simultaneously. Additionally, we propose a frequency domain constraint to optimize the locations for watermark embedding. Experimental results show that the proposed EIAW approach achieves attack effectiveness comparable to state-of-the-art methods while enabling accurate watermark extraction and maintaining high image quality. As a result, the EIAW approach is well-suited for a wide range of real-world applications, providing comprehensive protection for image copyright.
**Fig. 9**
Comparison of image quality over iterations for three strategies.
Show All
**Table 9** Comparison with the two-phase method in terms of ASR, EAR, and imperceptibility. Bold value indicates the best performance among different methods. “↑” means larger is better, while “↓” means smaller is better.
### ACKNOWLEDGMENT
This work was supported by the National Natural Science Foundation of China (Nos. 62372125 and 62476113), the Guangdong Natural Science Funds for Distinguished Young Scholar (No. 2023B1515020041), the Ministry of Science and Technology Xiongan New Area Science and Technology Innovation Special Sub-course (No. 2022XAGG0126), the Liaoning Collaboration Innovation Center For CSLE, the National College Student Innovation Training Program of Guangzhou University (No. 202411078002), and the Provincial College Student Innovation Training Program of Guangzhou University (No. 202511078077).
## Authors
## Figures
## References
## Keywords
## Metrics
## More Like This
[An enhanced time series anomaly detection model based on frequency domain analysis](https://ieeexplore.ieee.org/document/10762133/)
2024 5th International Conference on Big Data & Artificial Intelligence & Software Engineering (ICBASE)
Published: 2024
[Time Frequency Domain Analysis Model for Insulation Risk of Key Equipment in Substations under High-frequency Transient Interference](https://ieeexplore.ieee.org/document/11509396/)
2026 2nd International Conference on Power Electronics and Electric Drives (PEED)
Published: 2026
[Show More](javascript:void())
# References
**References is not available for this document.**
## IEEE Personal Account
* [Change username/password](https://www.ieee.org/profile/changeusrpwd/showChangeUsrPwdPage.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
## Purchase Details
* [Payment Options](https://www.ieee.org/profile/payment/showPaymentHome.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [View Purchased Documents](https://ieeexplore.ieee.org/articleSale/purchaseHistory.jsp)
## Profile Information
* [Communications Preferences](https://www.ieee.org/ieee-privacyportal/app/ibp?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [Profession and Education](https://www.ieee.org/profile/profedu/getProfEduInformation.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [Technical interests](https://www.ieee.org/profile/tips/getTipsInfo.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
## Need Help?
* [US & Canada: +1 800 678 4333](tel:+1-800-678-4333)
* [Worldwide: +1 732 981 0060](tel:+1-732-981-0060)
* [Contact & Support](https://ieeexplore.ieee.org/xpl/contact)
## Follow
[About IEEE *Xplore*](https://ieeexplore.ieee.org/Xplorehelp/overview-of-ieee-xplore/about-ieee-xplore) | [Contact Us](https://ieeexplore.ieee.org/xpl/contact) | [Help](https://ieeexplore.ieee.org/Xplorehelp) | [Accessibility](https://ieeexplore.ieee.org/Xplorehelp/overview-of-ieee-xplore/accessibility-statement) | [Terms of Use](https://ieeexplore.ieee.org/Xplorehelp/overview-of-ieee-xplore/terms-of-use) | [Nondiscrimination Policy](http://www.ieee.org/web/aboutus/whatis/policies/p9-26.html) | [IEEE Ethics Reporting](http://www.ieee-ethics-reporting.org/) | [Sitemap](https://ieeexplore.ieee.org/Xplorehelp/overview-of-ieee-xplore/ieee-xplore-sitemap) | [IEEE Privacy Policy](http://www.ieee.org/about/help/security_privacy.html)
A public charity, IEEE is the world's largest technical professional organization dedicated to advancing technology for the benefit of humanity.
© Copyright 2026 IEEE - All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies.
### IEEE Account
* [Change Username/Password](https://www.ieee.org/profile/changeusrpwd/showChangeUsrPwdPage.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [Update Address](https://www.ieee.org/profile/address/getAddrInfoPage.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
### Purchase Details
* [Payment Options](https://www.ieee.org/profile/payment/showPaymentHome.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [Order History](https://www.ieee.org/profile/vieworder/showOrderHistory.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [View Purchased Documents](https://ieeexplore.ieee.org/articleSale/purchaseHistory.jsp)
### Profile Information
* [Communications Preferences](https://www.ieee.org/ieee-privacyportal/app/ibp?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [Profession and Education](https://www.ieee.org/profile/profedu/getProfEduInformation.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
* [Technical Interests](https://www.ieee.org/profile/tips/getTipsInfo.html?refSite=https://ieeexplore.ieee.org&refSiteName=IEEE Xplore)
### Need Help?
* **US & Canada:** +1 800 678 4333
* **Worldwide:**  +1 732 981 0060
* [Contact & Support](https://ieeexplore.ieee.org/xpl/contact)
* [About IEEE *Xplore*](https://ieeexplore.ieee.org/Xplorehelp/overview-of-ieee-xplore/about-ieee-xplore)
* [Contact Us](https://ieeexplore.ieee.org/xpl/contact)
* [Help](https://ieeexplore.ieee.org/Xplorehelp)
* [Accessibility](https://ieeexplore.ieee.org/Xplorehelp/overview-of-ieee-xplore/accessibility-statement)
* [Terms of Use](https://ieeexplore.ieee.org/Xplorehelp/overview-of-ieee-xplore/terms-of-use)
* [Nondiscrimination Policy](http://www.ieee.org/web/aboutus/whatis/policies/p9-26.html)
* [Sitemap](https://ieeexplore.ieee.org/xpl/sitemap.jsp)
* [Privacy & Opting Out of Cookies](http://www.ieee.org/about/help/security_privacy.html)
A not-for-profit organization, IEEE is the world's largest technical professional organization dedicated to advancing technology for the benefit of humanity.
© Copyright 2026 IEEE - All rights reserved. Use of this web site signifies your agreement to the terms and conditions.
