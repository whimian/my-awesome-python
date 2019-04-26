import copy
from pathlib import Path
from PyPDF4 import PdfFileWriter,PdfFileReader,PdfFileMerger
from tqdm import trange


def print_box(page):
    # print('CropBox' + '-'*10)
    # print(page.cropBox.getLowerLeft())
    # print(page.cropBox.getLowerRight())
    # print(page.cropBox.getUpperLeft())
    # print(page.cropBox.getUpperRight())
    # print('TrimBox' + '-'*10)
    # print(page.trimBox.getLowerLeft())
    # print(page.trimBox.getLowerRight())
    # print(page.trimBox.getUpperLeft())
    # print(page.trimBox.getUpperRight())
    print("Width: {}".format(page.mediaBox.getWidth()))
    print("Height: {}".format(page.mediaBox.getHeight()))
    print('MediaBox' + '-'*10)
    print(page.mediaBox.getLowerLeft())
    print(page.mediaBox.getLowerRight())
    print(page.mediaBox.getUpperLeft())
    print(page.mediaBox.getUpperRight())
    # print('BleedBox' + '-'*10)
    # print(page.bleedBox.getLowerLeft())
    # print(page.bleedBox.getLowerRight())
    # print(page.bleedBox.getUpperLeft())
    # print(page.bleedBox.getUpperRight())
    # print('ArtBox' + '-'*10)
    # print(page.artBox.getLowerLeft())
    # print(page.artBox.getLowerRight())
    # print(page.artBox.getUpperLeft())
    # print(page.artBox.getUpperRight())

def cut_left(file_path, output_file, points=66):

    with open(str(file_path), 'rb') as pfl:
        in_pdf = PdfFileReader(pfl)
        out_pdf = PdfFileWriter()
        n_pages = in_pdf.getNumPages()

        for i in trange(n_pages):
            page = in_pdf.getPage(i)
            # print_box(page)
            p_width = page.mediaBox.getWidth()
            p_height = page.mediaBox.getHeight()

            if p_width > p_height:

                lower_left = page.mediaBox.getLowerLeft()
                lower_left = (lower_left[0]+points, lower_left[1]) #(55.479, 0)

                upper_left = page.mediaBox.getUpperLeft()
                upper_left = (upper_left[0]+points, upper_left[1]) #(55.479, 604.321)

                page.mediaBox.lowerLeft = lower_left
                page.mediaBox.upperLeft = upper_left


            else:
                upper_left = page.mediaBox.getUpperLeft()
                upper_left = (upper_left[0], upper_left[1] - points) #(55.479, 0)

                upper_right = page.mediaBox.getUpperRight()
                upper_right = (upper_right[0], upper_right[1] - points) #(55.479, 604.321)

                page.mediaBox.upperLeft = upper_left
                page.mediaBox.upperRight = upper_right


            page.artBox = page.mediaBox
            page.bleedBox = page.mediaBox
            page.cropBox = page.mediaBox
            # print_box(page)

            out_pdf.addPage(page)

        print("Writing file ...")
        with open(output_file, 'wb') as outfl:
            out_pdf.write(outfl)


def split_middle(file_path, output_file):

    with open(str(file_path), 'rb') as pfl:
        in_pdf = PdfFileReader(pfl)
        out_pdf = PdfFileWriter()
        n_pages = in_pdf.getNumPages()

        for i in range(n_pages):
            page = in_pdf.getPage(i)

            p_width = page.mediaBox.getWidth()
            p_height = page.mediaBox.getHeight()


            page1 = copy.copy(page)
            page1.mediaBox = copy.copy(page.mediaBox)
            page2 = copy.copy(page)
            page2.mediaBox = copy.copy(page.mediaBox)


            if p_width > p_height: # Because PDF page can be in vertical or horizontal orientation

                x0, y0 = page.mediaBox.getLowerLeft()
                x1, y1 = page.mediaBox.getUpperRight()
                # print(x0, x1, y0, y1)

                # (x0,y1) ---------- (x1,y1)
                #    |                  |
                #    |                  |
                #    |                  |
                # (x0,y0) ---------- (x1,y1)

                page1.mediaBox.lowerLeft = (x0, y0)
                page1.mediaBox.upperLeft = (x0, y1)
                page1.mediaBox.lowerRight = ((x0+x1)/2, y0)
                page1.mediaBox.upperRight = ((x0+x1)/2, y1)

                page2.mediaBox.lowerRight = (x0, y0)
                page2.mediaBox.upperRight = (x1, y1)
                page2.mediaBox.lowerLeft = ((x0+x1)/2, y0)
                page2.mediaBox.upperLeft = ((x0+x1)/2, y1)

            else:

                x0, y0 = page.mediaBox.getLowerLeft()
                x1, y1 = page.mediaBox.getUpperRight()

                page1.mediaBox.lowerLeft = (x0, (y0+y1)/2)
                page1.mediaBox.lowerRight = (x1, (y0+y1)/2)

                page2.mediaBox.upperLeft = (x0, (y0+y1)/2)
                page2.mediaBox.upperRight = (x1, (y0+y1)/2)

            page1.artBox = page1.mediaBox
            page1.bleedBox = page1.mediaBox
            page1.cropBox = page1.mediaBox

            page2.artBox = page2.mediaBox
            page2.bleedBox = page2.mediaBox
            page2.cropBox = page2.mediaBox

            out_pdf.addPage(page1)
            out_pdf.addPage(page2)

        print("Writing file ...")
        with open(output_file, 'wb') as outfl:
            out_pdf.write(outfl)

if __name__ == '__main__':

    file_path = Path("E:/My Documents/books2read/GeoStatistics/GSLIB_ Geostatistical Software Library and User's Guide (1997).pdf")

    cut_left(file_path, "C:/Users/yuhao/Desktop/test.pdf", points=66)

    # split_middle("C:/Users/yuhao/Desktop/test.pdf", "C:/Users/yuhao/Desktop/test2.pdf")
