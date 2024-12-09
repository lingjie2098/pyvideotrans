# 安装
双击[`for_macOS_install.command`](for_macOS_install.command)。
# 运行
双击[`for_macOS_start.command`](for_macOS_start.command)。
# 自定义配置
## CosyVoice参考音频过短的处理方案
[`_cosyvoice.py`](videotrans/tts/_cosyvoice.py)：
```py
...
                    if len(audio_chunk)<4000:
                        audio_chunk=audio_chunk*2
                        audio_chunk.export(data_item['ref_wav'],format='wav')
...
```
修改为：
```py
...
                    # 1倍 nothing to do
                    # 2倍
                    if len(audio_chunk)<4000:
                        audio_chunk=audio_chunk*2
                        audio_chunk.export(data_item['ref_wav'],format='wav')
                    # n倍
                    # if len(audio_chunk)<4000:
                    #     import math
                    #     audio_chunk=audio_chunk*math.ceil(4000/len(audio_chunk))
                    #     audio_chunk.export(data_item['ref_wav'],format='wav')
...
```
## F5-TTS参考音频过短的处理方案
[`_f5tts.py`](videotrans/tts/_f5tts.py)：
```py
...
                if len(audio_chunk)<4000:
                    audio_chunk=audio_chunk*2
                    audio_chunk.export(data_item['ref_wav'],format='wav')
                    data['ref_text']+=f". {data['ref_text']}"
...
```
修改为：
```py
...
                # 1倍 nothing to do
                # 2倍
                if len(audio_chunk)<4000:
                    audio_chunk=audio_chunk*2
                    audio_chunk.export(data_item['ref_wav'],format='wav')
                    data['ref_text']+=f". {data['ref_text']}"
                # n倍
                # if len(audio_chunk)<4000:
                #     import math
                #     i=math.ceil(4000/len(audio_chunk))
                #     audio_chunk=audio_chunk*i
                #     audio_chunk.export(data_item['ref_wav'],format='wav')
                #     data['ref_text']=". ".join([data['ref_text']]*i)
...
```
## 唇音不同步
[`_rate.py`](videotrans/task/_rate.py)：
```py
            able_time = self.queue_tts[i + 1]['start_time'] - it['start_time'] if i < length - 1 else raw_total_time - it['start_time']
```
修改为：
```py
            # able_time = self.queue_tts[i + 1]['start_time'] - it['start_time'] if i < length - 1 else raw_total_time - it['start_time']
            able_time = it['end_time'] - it['start_time']
```
## 配音首尾有静音段
1、菜单栏 --> 工具/选项 --> 高级选项 --> 移除配音末尾空白√
2、如果对效果不满意，调整
[`_base.py`](videotrans/tts/_base.py)：
```py
                    tools.remove_silence_from_end(it['filename'])
```
修改为：
```py
                    # tools.remove_silence_from_end(it['filename'])
                    tools.remove_silence_from_end(it['filename'], -40.0)    # 默认-50.0，声音越大，越接近0。谨慎起见，请使用默认值，修改容易导致一些轻音（比如it的发音）被消除。
```
