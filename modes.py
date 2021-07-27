import numpy as np
import cv2 as cv
class modes() :
    def __init__(self):
        pass
    def __init__(self, path):
        self.img = cv.imread(path,0)
        # self.imgByte = cv.imread(path, flags=cv.IMREAD_GRAYSCALE).T
        self.f = np.fft.fft2(self.img)
        self.fShift=np.fft.fftshift(self.f)
        self.mag = 20 * np.log(np.abs(self.fShift))
        self.phase = np.angle(self.fShift)
        self.real = 20 * np.log(np.real(self.fShift))
        self.imaginary = 20 * np.log(np.imag(self.fShift))
        self.imaginary[self.imaginary <= 0] = 10 ** -8
        self.reall = np.real(self.f)
        self.imaginaryy = np.imag(self.f)
        self.magnitudee = np.abs(self.f)
        self.phasee = np.angle(self.f)
        self.imgshape = self.img.shape
        self.uniformMagnitude = np.ones(self.img.shape)
        self.uniformPhase = np.zeros(self.img.shape)
    def mix(self, imageToBeMixed: 'modes', magnitudeRealoruniformmagRatio: float, phaseimageoruniformphaseRatio: float, comp1 , comp2 ):
        w1 = magnitudeRealoruniformmagRatio
        w2 = phaseimageoruniformphaseRatio
        self.first = comp1
        self.second = comp2
        mixInverse = None
        if (self.first == 'magnitude' and self.second == 'phase') or (self.first == 'phase' and self.second == 'magnitude'):
            mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * (imageToBeMixed.magnitudee) + w1 * (self.magnitudee)), np.exp(1j * (w2 * (imageToBeMixed.phasee) + (1 - w2) * (self.phasee))))))
        elif (self.first == 'magnitude' and self.second == 'uniform phase') or (self.first == 'uniform phase' and self.second == 'magnitude'):
            mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * (imageToBeMixed.magnitudee) + w1 * (self.magnitudee)), np.exp(1j * (w2 * (imageToBeMixed.uniformPhase) + (1 - w2) * (self.uniformPhase))))))
        elif (self.first == 'phase' and self.second == 'uniform magnitude') or (self.first == 'uniform magnitude' and self.second == 'phase'):
            mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * (imageToBeMixed.uniformMagnitude) + w1 * (self.uniformMagnitude)), np.exp(1j * (w2 * (imageToBeMixed.phasee) + (1 - w2) * (self.phasee))))))
        elif (self.first == 'real' and self.second =='imaginary') or (self.first == 'imaginary' and self.second =='real'):
            mixInverse = np.real(np.fft.ifft2((w1*(self.reall) + (1-w1)*(imageToBeMixed.reall)) + ((1-w2)*(self.imaginaryy) + w2*(imageToBeMixed.imaginaryy)) * 1j))
        if(self.first == 'real' and self.second =='imaginary') or (self.first == 'imaginary' and self.second =='real'):
            return abs(mixInverse)
        else:
            return abs(mixInverse1)

        # elif (self.first == 'magnitude' and self.second =='uniform phase') or (self.first == 'uniform phase' and self.second =='magnitude'):
        #     print("Mixing magnitude and uniformPhase")
        #     m1 = self.magnitudee
        #     m2 = imageToBeMixed.magnitudee
        #     up1 = self.uniformPhase
        #     up2 = imageToBeMixed.uniformPhase
        #     magMix = w1 * m1 + (1 - w1) * m2
        #     upMix = (1 - w2) * up1 + w2 * up2
        #     combined = np.multiply(magMix, np.exp(1j * upMix))
        #     mixInverse = np.real(np.fft.ifft2(combined))
        # elif (self.first == 'phase' and self.second =='uniform magnitude') or (self.first == 'uniform magnitude' and self.second =='phase'):
        #     print("Mixing phase and uniformmagnitude")
        #     p1 = self.phasee
        #     p2 = imageToBeMixed.phasee
        #     um1 = self.uniformMagnitude
        #     um2 = imageToBeMixed.uniformMagnitude
        #     phMix = w2 * p2 + (1 - w2) * p1
        #     umMix = (1 - w1) *  um2 + w1 *  um1
        #     combined=np.multiply(umMix, np.exp(1j * phMix))
        #     mixInverse = np.real(np.fft.ifft2(combined))
        # elif (self.first == 'uniform magnitude' and self.second =='uniform phase') or (self.first == 'uniform phase' and self.second =='uniform magnitude'):
        #     print("Mixing uniform phase and uniformmagnitude")
        #     up1 = self.uniformPhase
        #     up2 = imageToBeMixed.uniformPhase
        #     um1 = self.uniformMagnitude
        #     um2 = imageToBeMixed.uniformMagnitude
        #     uphMix = w2 * up2 + (1 - w2) * up1
        #     umMix = (1 - w1) *  um2 + w1 *  um1
        #     combined=np.multiply(umMix, np.exp(1j * uphMix))
        #     mixInverse = np.real(np.fft.ifft2(combined))

        # return abs(mixInverse)

# def mix(self, imageToBeMixed: 'modes', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, comp1, comp2):
#     w1 = magnitudeOrRealRatio
#     w2 = phaesOrImaginaryRatio
#     self.first = comp1
#     self.second = comp2
#     mixInverse = None
#     if (self.first == 'magnitude' and self.second == 'phase') or (self.first == 'phase' and self.second == 'magnitude'):
#         print("Mixing Magnitude and Phase")
#         m1 = self.magnitudee
#         m2 = imageToBeMixed.magnitudee
#         p1 = self.phasee
#         p2 = imageToBeMixed.phasee
#         # mix1 = w1*m1 + (1-w1)*m2
#         # mix2 = (1-w2)*P1 + w2*P2
#         # combined = np.multiply(mix1, np.exp(1j * mix2))
#         # mixInverse = np.real(np.fft.ifft2(combined))
#     elif (self.first == 'magnitude' and self.second == 'uniform phase') or (self.first == 'uniform phase' and self.second == 'magnitude'):
#         print("Mixing magnitude and uniformPhase")
#         m1 = self.magnitudee
#         m2 = imageToBeMixed.magnitudee
#         p1 = self.uniformPhase
#         p2 = imageToBeMixed.uniformPhase
#         # mix1 = w1 * m1 + (1 - w1) * m2
#         # mix2 = (1 - w2) * p1 + w2 * p2
#     # combined = np.multiply(mix1, np.exp(1j * mix2))
#     # mixInverse = np.real(np.fft.ifft2(combined))
#     elif (self.first == 'phase' and self.second == 'uniform magnitude') or (
#             self.first == 'uniform magnitude' and self.second == 'phase'):
#         print("Mixing phase and uniformmagnitude")
#         p1 = self.phasee
#         p2 = imageToBeMixed.phasee
#         m1 = self.uniformMagnitude
#         m2 = imageToBeMixed.uniformMagnitude
#     mix2 = w2 * p2 + (1 - w2) * p1
#     mix1 = (1 - w1) * m2 + w1 * m1
#     combined = np.multiply(mix1, np.exp(1j * mix2))
#     mixInverse = np.real(np.fft.ifft2(combined))
# return abs(mixInverse)
#     elif (self.first == 'real' and self.second == 'imaginary') or (self.first == 'imaginary' and self.second == 'real'):
#     print("Mixing Real and Imaginary")
#     R1 = self.reall
#     R2 = imageToBeMixed.reall
#     I1 = self.imaginaryy
#     I2 = imageToBeMixed.imaginaryy
#     realMix = w1 * R1 + (1 - w1) * R2
#     imaginaryMix = (1 - w2) * I1 + w2 * I2
#     combined = realMix + imaginaryMix * 1j
#     mixInverse = np.real(np.fft.ifft2(combined))
#
#
# return abs(mixInverse)





    # def mix(self, imageToBeMixed: 'modes', magnitudeRealoruniformmagRatio: float, phaseimageoruniformphaseRatio: float, comp1 , comp2 ):
    #     w1 = magnitudeRealoruniformmagRatio
    #     w2 = phaseimageoruniformphaseRatio
    #     self.first = comp1
    #     self.second = comp2
    #     mixInverse = None
    #     if (self.first == 'magnitude' and self.second == 'phase') or (self.first == 'phase' and self.second == 'magnitude'):
    #         print("Mixing Magnitude and Phase")
    #         m1 = self.magnitudee
    #         m2 = imageToBeMixed.magnitudee
    #         p1 = self.phasee
    #         p2 = imageToBeMixed.phasee
    #     elif (self.first == 'magnitude' and self.second == 'uniform phase') or (self.first == 'uniform phase' and self.second == 'magnitude'):
    #         print("Mixing magnitude and uniformPhase")
    #         m1 = self.magnitudee
    #         m2 = imageToBeMixed.magnitudee
    #         p1 = self.uniformPhase
    #         p2 = imageToBeMixed.uniformPhase
    #     elif (self.first == 'phase' and self.second == 'uniform magnitude') or (self.first == 'uniform magnitude' and self.second == 'phase'):
    #         print("Mixing phase and uniformmagnitude")
    #         p1 = self.phasee
    #         p2 = imageToBeMixed.phasee
    #         m1 = self.uniformMagnitude
    #         m2 = imageToBeMixed.uniformMagnitude
    #     elif (self.first == 'real' and self.second =='imaginary') or (self.first == 'imaginary' and self.second =='real'):
    #         print("Mixing Real and Imaginary")
    #         R1 = self.reall
    #         R2 = imageToBeMixed.reall
    #         I1 = self.imaginaryy
    #         I2 = imageToBeMixed.imaginaryy
    #         realMix = w1*R1 + (1-w1)*R2
    #         imaginaryMix = (1-w2)*I1 + w2*I2
    #         combined = realMix + imaginaryMix * 1j
    #         mixInverse = np.real(np.fft.ifft2(combined))
    #     if(self.first == 'real' and self.second =='imaginary') or (self.first == 'imaginary' and self.second =='real'):
    #         return abs(mixInverse)
    #     else:
    #         # mix2 = w2 * p2 + (1 - w2) * p1
    #         # mix1 = (1 - w1) * m2 + w1 * m1
    #         # combined1 = np.multiply(mix1, np.exp(1j * mix2))
    #         mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * m2 + w1 * m1), np.exp(1j * (w2 * p2 + (1 - w2) * p1)))))
    #         return abs(mixInverse1)