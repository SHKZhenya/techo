import os

import telebot
bot = telebot.TeleBot('6704729507:AAFN0t8iG5UBha036-nZIHn02dt2ycnlo1I')

from random import randint

from PIL import Image, ImageDraw

from time import sleep

@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = message.document.file_name  # сохраняем файл с его исходным именем
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        if '.png' not in message.document.file_name:
            bot.send_message(message.from_user.id, 'Файл должен иметь расширение PNG!')
            return
        bot.send_message(message.from_user.id, 'Идет процесс дешифрования...')
        print(new_file)
        img = Image.open(message.document.file_name)
        print(img)
        pix = img.load()
        print(5)
        w, h = img.size[0], img.size[1] #строки, столбцы
        tek = 0
        ans = ''
        d = 0
        print(w, h)
        for _ in range(10):
            i, j = tek // h, tek % h
            ans += str(pix[i, j][d] % 2)
            print(i, j, d, pix[i, j])
            tek += 31
            tek %= (w * h)
            d += 1
            d %= 3
        print(ans)
        crv = int(ans, 2)
        ans = ''
        for i in range(crv):
            i, j = tek // h, tek % h
            ans += str(pix[i, j][d] % 2)
            print(i, j, d, pix[i, j])
            tek += 31
            tek %= (w * h)
            d += 1
            d %= 3
        c = int(ans[-5:], 2)
        ans = ans[:-5]
        l = ''
        for i in range(0, len(ans), c):
            pr = ans[i:i + c]
            pr = int(pr, 2)
            l += chr(pr)
        print(l)
        bot.send_message(message.from_user.id, l)
        os.remove(message.document.file_name)
        sleep(1)
        #
        # # Отправить в дальнейшем можно таким образом
        # #bot.send_photo(message.chat.id, photo=photo_bytes)
    except:
        s = message.text
        if s == "/start":
            hello = "Приветствую тебя, дорогой мой друг!\n1) Отправь любую фразу боту, а он тебе выдаст стеганографическую картинку с котиком!\n2) Отправь боту картинку формата PNG, и он тебе выдаст то, что закодировано на этой картинке! (Вы можете пересылать картинки)"
            bot.send_message(message.from_user.id, hello)
            return
        # print('text', s)
        if len(s) > 1000:
            bot.send_message(message.from_user.id, 'Введите сообщение не длиннее 1000 символов')
            return
        bot.send_message(message.from_user.id, 'Идет процесс шифрования...')
        l = []
        mx = -1
        for i in s:
            l.append(ord(i))
            mx = max(mx, l[-1])
        #print(l, mx, bin(mx))
        b = bin(mx)[2:]
        ln = len(b)
        #print(ln)
        cnt = ['0' for i in range(ln * len(s))]
        tek = -1
        # print(l)
        for i in range(ln * len(s) - 1, -1, -ln):
            for j in range(i, i - ln, -1):
                cnt[j] = str(l[tek] % 2)
                l[tek] //= 2
            tek -= 1
        # print(cnt)
        bnd = bin(ln)[2:]
        bnd = (5 - len(bnd)) * '0' + bnd
        cnt += list(bnd)
        # print(cnt)
        crv = bin(len(cnt))[2:]
        crv = (10 - len(crv)) * '0' + crv
        crv = list(crv)
        #print(len(cnt))
        cnt = crv + cnt
        ct = randint(1, 43)
        image = Image.open("cats/cat" + str(ct) + '.jpg')
        # print(image)
        draw = ImageDraw.Draw(image)
        w, h = image.size[0], image.size[1] #строки, столбцы
        pix = image.load()
        px = image.load()
        #print(pix[w - 1, h - 1])
        pr = 31
        cnt += ['1' for _ in range(15)]
        tek = 0
        d = 0
        # print(pix)
        for i in range(w):
            for j in range(h):
                if (i * h + j) % 31 == 0:
                    ct = (i * h + j) // 31
                    if ct < len(cnt):
                        por = [pix[i, j][0], pix[i, j][1], pix[i, j][2]]
                        if cnt[ct] == '0':
                            if por[d] % 2 == 1:
                                por[d] -= 1
                            else:
                                pass
                        else:
                            if por[d] % 2 == 0:
                                por[d] += 1
                            else:
                                pass
                        draw.point((i, j), (por[0], por[1], por[2]))
                        # print(i, j, por)
                        d += 1
                        d %= 3
                    else:
                        draw.point((i, j), pix[i, j])
                else:
                    draw.point((i, j), pix[i, j])
            # i, j = tek // h, tek % h
            # por = [pix[i, j][0], pix[i, j][1], pix[i, j][2]]
            # if cnt[x] == '0':
            #     if por[d] % 2 == 1:
            #         por[d] -= 1
            #     else:
            #         pass
            # else:
            #     if por[d] % 2 == 0:
            #         por[d] += 1
            #     else:
            #         pass
            # print(i, j, por)
            # tek += 1
            # i, j = tek // h, tek % h
            # while tek % 31 != 0:
            #     draw.point((i, j), (por[0], por[1], por[2]))
            #     i, j = tek // h, tek % h
            #     tek += 1
            # d += 1
            # d %= 3
        image.save("cat.png", 'PNG')
        image = Image.open("cat.png")
        # print(image)
        px = image.load()
        # print(px == pix)
        # print(px[0, 0], px[0, 31])
        bot.send_document(message.from_user.id, open("cat.png", "rb"))
        os.remove("cat.png")
        # print(''.join(i for i in cnt))
        # print(w, h)



bot.polling(none_stop=True, interval=0)