---
layout: post
title: "Bài 0.20: Kiểm tra giả định mô hình cơ bản"
chapter: '00'
order: 20
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách kiểm tra có hệ thống các giả định cốt lõi của mô hình (dạng phân phối, tính độc lập, cấu trúc sai số), nhận diện sớm dấu hiệu sai đặc tả mô hình (misspecification), và chuyển kết quả chẩn đoán thành bước cải tiến mô hình cụ thể.

## 1) Giả định mô hình là gì và nằm ở đâu?

**Mỗi mô hình thống kê đều ngầm giả định dữ liệu phát sinh từ một cơ chế nhất định, nhiễu mang một cấu trúc cụ thể, và mối liên hệ giữa biến đầu vào với biến đầu ra có một dạng hình học hoặc xác suất xác định.**

Trong thực hành, giả định thường nằm ở ba lớp:
- **Hàm hợp lý (likelihood)**: dữ liệu thuộc họ phân phối nào (Gaussian, Poisson, Binomial...).
- **Cấu trúc trung bình (mean structure)**: mối quan hệ giữa $$x$$ và kỳ vọng của $$y$$ là tuyến tính, phi tuyến hay có tương tác.
- **Cấu trúc nhiễu (noise structure)**: phương sai có đồng nhất hay thay đổi theo giá trị dự báo, và các quan sát có phụ thuộc theo thời gian hay theo nhóm không.

## 2) Bộ kiểm tra tối thiểu nên thực hiện

### 2.1 Kiểm tra phân phối đầu ra

1. Vẽ histogram hoặc đường ước lượng mật độ của $$y$$.
2. Đối chiếu hình dạng dữ liệu với hàm hợp lý dự định dùng.
3. Kiểm tra các đặc điểm nổi bật: dữ liệu có lệch mạnh, có nhiều giá trị 0, hay bị giới hạn miền (như đoạn $$[0,1]$$) không?

Ví dụ, dữ liệu đếm chứa nhiều giá trị 0 thường không phù hợp với phân phối Gaussian; dữ liệu tỷ lệ trên $$[0,1]$$ cần mô hình tôn trọng miền giá trị thay vì dự báo vượt ngoài khoảng hợp lệ.

### 2.2 Kiểm tra phần dư

Phần dư (residual) được định nghĩa là:

$$
e_i = y_i - \hat y_i
$$

Ở đây, $$e_i$$ là chênh lệch giữa giá trị quan sát thật $$y_i$$ và giá trị mô hình dự báo $$\hat y_i$$: nếu $$e_i > 0$$, mô hình dự báo thấp hơn thực tế; nếu $$e_i < 0$$, mô hình dự báo cao hơn thực tế.

Cần phân biệt rõ $$e_i$$ và $$\epsilon_i$$. Trong mô hình sinh dữ liệu $$y_i = \mu_i + \epsilon_i$$, $$\epsilon_i$$ là **sai số thật không quan sát trực tiếp được**, còn $$e_i = y_i - \hat y_i$$ là **phần dư tính sau khi khớp mô hình**, đóng vai trò công cụ chẩn đoán thực hành. Khi mô hình phù hợp, hành vi của $$e_i$$ gần với $$\epsilon_i$$, nhưng hai đại lượng này không hoàn toàn trùng nhau vì $$\hat y_i$$ được ước lượng từ chính dữ liệu.

Với một mô hình tạm ổn, phần dư cần dao động quanh 0, không thể hiện xu hướng có hệ thống theo $$\hat y$$ hay $$x$$, và không lộ ra cấu trúc rõ rệt như đường cong, hình phễu hay các cụm tách biệt theo nhóm.

![Residual check để nhìn xu hướng phần dư]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_residual_check.png)

*Hình 1a: Biểu đồ phần dư (residual plot) giúp kiểm tra nhanh xem phần dư có dao động quanh 0 hay đang lộ ra cấu trúc bất thường.*

### 2.3 Kiểm tra giá trị ngoại lai và điểm ảnh hưởng mạnh

Không phải giá trị ngoại lai (outlier) nào cũng là dữ liệu "hỏng". Chúng có thể là lỗi nhập liệu, trường hợp hiếm nhưng hợp lệ, hoặc tín hiệu cho thấy mô hình đang thiếu biến giải thích hay chọn sai hàm hợp lý. Bước quan trọng là kiểm tra độ nhạy: khi loại bỏ hoặc giảm trọng số một vài điểm ảnh hưởng mạnh, kết luận có thay đổi đáng kể không?

![Fit tuyến tính và các điểm có thể là outlier]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_fit_outliers.png)

*Hình 1b: Quan sát đường khớp cùng các điểm nằm xa xu hướng chung giúp phát hiện giá trị ngoại lai và điểm ảnh hưởng mạnh trước khi chỉnh sửa mô hình.*

### 2.4 Kiểm tra giả định độc lập

Giả định độc lập rất dễ bị vi phạm trong dữ liệu thực, phổ biến nhất ở ba dạng: phụ thuộc theo **thời gian** (tự tương quan), theo **nhóm** (như học sinh cùng lớp hoặc bệnh nhân cùng bệnh viện), và theo **không gian** (các điểm đo gần nhau thường tương đồng hơn). Nếu bỏ qua sự phụ thuộc này, khoảng bất định ước lượng thường bị thu hẹp quá mức lạc quan.

## 3) Bản đồ "dấu hiệu -> hành động"

Đây không phải quy tắc máy móc "thấy A thì bắt buộc dùng B", mà là trình tự suy luận: quan sát dấu hiệu từ dữ liệu hoặc phần dư, xác định giả định đang bị nghi ngờ, rồi thử điều chỉnh nhỏ nhất nhưng trúng trọng tâm:

**Phần dư có dạng đường cong**
- Nghi ngờ: cấu trúc trung bình (mean structure) chưa phù hợp — quan hệ giữa biến đầu vào và đầu ra không còn tuyến tính đơn giản.
- Hướng xử lý thử trước: thêm thành phần phi tuyến như `x^2`, `log(x)`, spline, hoặc thêm số hạng tương tác.

**Phần dư mở rộng hình phễu**
- Nghi ngờ: phương sai sai số không đồng nhất (heteroscedasticity), độ nhiễu tăng theo mức dự báo.
- Hướng xử lý thử trước: biến đổi thang đo như `log(y)`, chuyển sang hàm hợp lý phù hợp với dữ liệu lệch, hoặc mô hình hóa trực tiếp phương sai thay đổi.

**Xuất hiện nhiều giá trị cực đoan hơn dự kiến**
- Nghi ngờ: hàm hợp lý hiện tại có đuôi quá mỏng (chẳng hạn Gaussian rất nhạy với ngoại lai).
- Hướng xử lý thử trước: rà soát lỗi dữ liệu và biến bị bỏ sót, sau đó cân nhắc hàm hợp lý đuôi dày như Student-t thay cho Gaussian.

**Dữ liệu đếm có quá nhiều số 0 hoặc phương sai lớn hơn trung bình rõ rệt**
- Nghi ngờ: phân phối Poisson quá chặt so với độ phân tán thực tế.
- Hướng xử lý thử trước: chuyển sang Negative Binomial khi có quá phân tán (overdispersion); nếu số 0 dư thừa xuất phát từ cơ chế riêng, cân nhắc mô hình zero-inflated hoặc hurdle.

**Dữ liệu phân cụm theo nhóm hoặc phụ thuộc theo thời gian**
- Nghi ngờ: giả định độc lập giữa các quan sát bị vi phạm.
- Hướng xử lý thử trước: bổ sung cấu trúc phân cấp theo nhóm, hiệu ứng ngẫu nhiên (random effects), hoặc mô hình tương quan theo thứ tự thời gian.

Tóm lại, hãy sửa đúng giả định đang hỏng thay vì chọn mô hình theo xu hướng: phần dư cong là vấn đề **mean structure**, hình phễu là vấn đề **noise structure**, nhiều số 0 hoặc đuôi dày là vấn đề **likelihood**, còn phân cụm theo nhóm/thời gian là vấn đề **tính độc lập**.

## 4) Ví dụ dữ liệu thực tế: Nêu rõ nguồn số liệu và suy luận

Để minh họa cụ thể thay vì nhận xét cảm tính, phần này dùng các tập dữ liệu công khai trong Python (`seaborn.load_dataset`) theo quy trình bốn bước: nêu rõ dữ liệu và câu hỏi, khớp một mô hình cơ sở (baseline) đơn giản, kiểm tra giả định bằng chỉ số định lượng và biểu đồ phần dư, rồi đề xuất cập nhật đúng trọng tâm.

### Ví dụ 1: Dữ liệu `diamonds` (giá kim cương)

**Nguồn dữ liệu**: `seaborn.load_dataset("diamonds")`, gồm $$n=53{,}940$$ quan sát.

**Câu hỏi**: nếu bắt đầu với một biến giải thích duy nhất là trọng lượng `carat`, mô hình nào mô tả giá `price` ở mức hợp lý và những giả định nào hỏng trước tiên?

Đây là dạng dữ liệu thực rất phổ biến: biến đầu ra dương, lệch phải mạnh và độ biến động tăng theo giá trị trung bình. Khớp thẳng mô hình Gaussian tuyến tính trên thang giá gốc dễ vi phạm đồng thời cả cấu trúc trung bình lẫn cấu trúc nhiễu.

Bảng dưới đây trích 7 quan sát thật ở các mốc phân vị khác nhau của `price` (sau khi sắp xếp tăng dần), cho thấy `price` tăng nhanh theo `carat` đồng thời còn chịu ảnh hưởng của `cut`, `color` và `clarity`:

| Mốc trong phân phối giá | carat | cut | color | clarity | price (USD) |
| --- | ---: | --- | --- | --- | ---: |
| 0% | 0.23 | Ideal | E | SI2 | 326 |
| 10% | 0.31 | Ideal | H | VS2 | 646 |
| 30% | 0.42 | Premium | H | VS1 | 1087 |
| 50% | 0.58 | Ideal | F | VVS2 | 2401 |
| 70% | 1.02 | Ideal | I | VS2 | 4662 |
| 90% | 1.51 | Very Good | H | VS2 | 9821 |
| 98% | 2.43 | Very Good | H | SI2 | 16170 |

**Bước 1 — Kiểm tra phân phối đầu ra**: trên dữ liệu thực, `price` có `min = 326`, `median = 2401`, `max = 18823`, độ lệch `skewness = 1.618`, và phân vị thứ 95 ở mức `13107.1`.

- Chênh lệch lớn giữa `median = 2401` và `max = 18823` cho thấy đuôi phải kéo rất dài.
- `skewness = 1.618` xác nhận định lượng mức độ lệch phải rõ rệt.
- Mốc phân vị 95% ở `13107.1` cho thấy nhóm nhỏ quan sát ở đuôi cao có thể tác động mạnh tới đường khớp nếu chọn sai mô hình.

### Quyết định thực hành từ các chỉ số mô tả

Với phân phối dương và lệch phải mạnh như trên, một bước thử hợp lý là chuyển sang mô hình hóa trên thang `log(price)` trước khi tăng độ phức tạp. Phép biến đổi log giúp nén đuôi phải và ổn định phương sai hơn, tạo điểm khởi đầu tốt hơn để chẩn đoán tiếp. Các thống kê mô tả đầu vào nhờ đó dẫn thẳng tới hành động mô hình hóa cụ thể.

![Diamonds price distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_distribution.png)

*Hình 2: Histogram giá kim cương (`diamonds`) kèm mốc phân vị q95, thể hiện phân phối lệch phải rõ rệt với đuôi cao kéo dài.*

**Bước 2 — Khớp mô hình cơ sở và kiểm tra phần dư**: ta khớp mô hình cơ sở đơn giản để làm mốc chẩn đoán:

$$
y_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = \alpha + \beta\,\text{carat}_i
$$

Tương đương $$y_i = \mu_i + \epsilon_i$$ với $$\epsilon_i \sim \mathcal{N}(0,\sigma)$$. Mô hình này giả định: (1) giá trung bình tăng tuyến tính theo `carat`, và (2) phương sai sai số không đổi trên toàn miền dự báo.

Chẩn đoán định lượng trên phần dư $$e_i = y_i - \hat y_i$$ cho thấy:

- $$\mathrm{corr}(\lvert e_i \rvert, \hat y_i)=0.579$$: tương quan dương mạnh, nghĩa là giá trị dự báo càng lớn thì độ lớn phần dư càng tăng.
- MAE ở nhóm dự báo thấp và cao lần lượt là `478.4` và `2059.1`, chênh nhau `4.30` lần.

Sự mở rộng sai số có hệ thống này cho thấy giả định **đồng nhất phương sai** bị vi phạm rõ rệt — hoàn toàn khớp với trực giác thực tế rằng sai số 500 USD là lớn với viên kim cương giá 700 USD nhưng nhỏ với viên giá 10,000 USD.

![Diamonds residual vs fitted]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_residuals.png)

*Hình 3: Biểu đồ phần dư theo giá trị dự báo (residual vs fitted) của mô hình cơ sở trên `diamonds`, cho thấy độ phân tán mở rộng hình phễu khi dự báo tăng (dấu hiệu heteroscedasticity).*

**Bước 3 — Cập nhật mô hình và kiểm tra lại**: ta điều chỉnh trực tiếp vào hai điểm hỏng vừa phát hiện:

$$
\log y_i = \alpha + \beta_1\,\text{carat}_i + \beta_2\,\text{carat}_i^2 + \epsilon_i,
$$

trong đó lấy `log(y)` chuyển sai số mang tính tỷ lệ về dạng cộng tính ổn định hơn, còn số hạng `carat^2` cho phép quan hệ trung bình có độ cong.

Sau khi cập nhật, $$\mathrm{corr}(\lvert e_i \rvert, \hat y_i)$$ giảm từ `0.579` xuống `0.047` và tỷ lệ MAE cao/thấp giảm từ `4.30` xuống `1.16`. Cả hai chỉ số đều cho thấy độ phân tán phần dư giữa vùng giá thấp và vùng giá cao đã cân bằng hơn nhiều. Kết luận ở đây không phải mô hình log bậc hai là "đúng tuyệt đối", mà là quy trình kiểm tra giả định đã chỉ đúng chỗ hỏng và xác nhận cải thiện bằng cùng bộ tiêu chí.

---

### Ví dụ 2: Dữ liệu `taxis` (đếm số chuyến theo khu vực và ngày)

**Nguồn dữ liệu**: `seaborn.load_dataset("taxis")`.

**Câu hỏi**: khi tổng hợp số chuyến theo từng `pickup_zone` và từng ngày, phân phối Poisson có phải là mô hình cơ sở phù hợp cho biến đếm `trips` hay không?

**Cách tạo biến đếm**:
1. Lọc các chuyến có `pickup_borough = Manhattan`.
2. Gộp theo cặp `(pickup_zone, day)` để đếm số chuyến `trips`.
3. Điền đầy đủ mọi tổ hợp khu vực–ngày để giữ lại các ngày có 0 chuyến.

Kết quả thu được $$n=1953$$ ô quan sát khu vực–ngày, mỗi ô là một số đếm nguyên không âm.

**Bước 1 — Kiểm tra giả định cơ bản của Poisson**: nếu $$Y \sim \mathrm{Poisson}(\lambda)$$ thì kỳ vọng và phương sai phải bằng nhau:

$$
\mathbb{E}[Y] = \mathrm{Var}(Y).
$$

Trên dữ liệu thực, `mean(trips) = 2.697` nhưng `var(trips) = 7.441`, cho tỷ lệ `var/mean = 2.76` — độ phân tán lớn gần gấp 3 lần mức Poisson cho phép. Đây là dấu hiệu rõ ràng của **quá phân tán (overdispersion)**, xuất phát từ sự chênh lệch lớn về mật độ khách giữa các khu vực và giữa các ngày khác nhau.

![Taxis trip-count distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_distribution.png)

*Hình 4: Phân phối số chuyến theo khu vực–ngày trong dữ liệu `taxis`, kèm các chỉ số mean, variance và tỷ số var/mean thể hiện quá phân tán.*

**Bước 2 — Kiểm tra tỷ lệ số 0 và đuôi phải**: với Poisson, một tham số $$\lambda$$ duy nhất quy định đồng thời trung bình, xác suất bằng 0 và xác suất đuôi phải:

- Tỷ lệ bằng 0 quan sát được là $$P(Y=0)=0.245$$, trong khi Poisson với $$\lambda=2.697$$ chỉ dự báo $$P(Y=0)=e^{-\lambda}=0.067$$ — thực tế nhiều hơn khoảng $$0.245 / 0.067 \approx 3.7$$ lần.
- Ở đuôi phải, tỷ lệ quan sát được là $$P(Y\ge 10)=0.0261$$, trong khi Poisson chỉ dự báo $$0.00050$$ — thực tế lớn hơn khoảng 52 lần.

Như vậy, phân phối Poisson một tham số quá hẹp: khi khớp trung bình, nó đồng thời đánh giá thấp cả xác suất ngày vắng (0 chuyến) lẫn xác suất ngày rất đông ($$\ge 10$$ chuyến).

![Observed vs model implied probabilities on taxis]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_probabilities.png)

*Hình 5: So sánh xác suất quan sát với xác suất suy ra từ Poisson và Negative Binomial tại hai mốc mục tiêu $$P(Y=0)$$ và $$P(Y\ge 10)$$.*

**Bước 3 — Cập nhật và kiểm tra lại**: với dữ liệu đếm quá phân tán, Negative Binomial là bước mở rộng tự nhiên vì cho phép phương sai lớn hơn trung bình (tương đương việc cho tốc độ sinh chuyến biến thiên giữa các khu vực–ngày).

Ước lượng Negative Binomial theo phương pháp khớp mô-men (moment matching) cho tham số phân tán $$k=1.534$$, dự báo $$P(Y=0)=0.211$$ (gần mức quan sát `0.245`) và $$P(Y\ge 10)=0.0279$$ (rất sát mức quan sát `0.0261`). Lựa chọn Negative Binomial ở đây có cơ sở chẩn đoán rõ ràng vì nó khắc phục đồng thời ba điểm yếu của Poisson: phương sai vượt trung bình, tỷ lệ 0 cao và đuôi phải dày.

---

### Điều cần rút ra từ hai ví dụ

1. Bắt đầu bằng một mô hình cơ sở đủ đơn giản để thấy rõ toàn bộ giả định đang đặt ra.
2. Gắn nhận xét trực quan với chỉ số định lượng cụ thể (`skewness`, `var/mean`, tương quan phần dư, xác suất bằng 0 và đuôi).
3. Cập nhật đúng giả định bị vi phạm (biến đổi thang đo/thêm độ cong cho mean và noise structure; đổi hàm hợp lý khi phân phối đếm quá phân tán).
4. Kiểm chứng lại mô hình mới bằng chính bộ tiêu chí chẩn đoán ban đầu.

## 5) Quy trình 15 phút trước khi tin vào kết quả mô hình

1. Xem phân phối của biến đầu ra.
2. Khớp một mô hình đơn giản làm mốc cơ sở.
3. Vẽ biểu đồ phần dư theo giá trị dự báo và theo các biến giải thích chính.
4. Tìm điểm ảnh hưởng mạnh và kiểm tra độ nhạy của kết luận.
5. Kiểm tra dấu hiệu phụ thuộc theo thời gian hoặc theo nhóm.
6. Ghi nhận 1–2 giả định có rủi ro cao nhất.
7. Cập nhật mô hình và đối chiếu lại các chỉ số chẩn đoán.

Mục tiêu của quy trình này là giảm rủi ro suy luận sai, không phải vẽ thật nhiều biểu đồ hình thức.

## 6) Sai mô hình không phải thất bại, mà là tín hiệu cập nhật

Trong quy trình làm việc Bayesian (Bayesian workflow), xây dựng mô hình là một vòng lặp:

1. Đề xuất mô hình.
2. Khớp mô hình với dữ liệu.
3. Kiểm tra giả định và hệ quả dự báo.
4. Cải tiến mô hình.

Mục tiêu không phải chứng minh mô hình "đúng tuyệt đối", mà là làm cho mô hình ngày càng phù hợp hơn với dữ liệu và câu hỏi nghiên cứu.

## Tóm tắt nhanh

1. Mọi mô hình thống kê đều đi kèm các giả định cụ thể.
2. Giả định bị vi phạm nặng có thể dẫn đến kết luận sai lệch.
3. Bộ kiểm tra tối thiểu gồm: phân phối đầu ra, phần dư, ngoại lai/điểm ảnh hưởng và tính độc lập.
4. Dấu hiệu sai đặc tả cần được chuyển thành điều chỉnh cụ thể ở hàm hợp lý hoặc cấu trúc mô hình.
5. Sai mô hình là thông tin chẩn đoán để cải tiến, không phải thất bại.

## Video tham khảo

- [Quantile-Quantile Plots (QQ plots), Clearly Explained!!!](https://www.youtube.com/watch?v=okjYjClSjOg) — StatQuest with Josh Starmer, English. **Xem trước.** Giải thích cách dùng biểu đồ Q–Q để đối chiếu phân phối phần dư với phân phối giả định.
- [Simple Linear Regression:  Checking Assumptions with Residual Plots](https://www.youtube.com/watch?v=iMdtTCX2Q70) — jbstatistics, English. Minh họa các dạng biểu đồ phần dư và cách nhận diện giả định bị vi phạm.
- [Lecture37 (Data2Decision) Independence of Residuals](https://www.youtube.com/watch?v=ADICTMUvPg0) — Chris Mack, English. Trình bày giả định độc lập của phần dư và các dấu hiệu tự tương quan.

## Câu hỏi tự luyện

1. Nêu một tình huống thực tế vi phạm giả định độc lập và đề xuất hướng điều chỉnh mô hình.
2. Vì sao biểu đồ phần dư theo giá trị dự báo giúp phát hiện sai cấu trúc trung bình?
3. Khi gặp giá trị ngoại lai mạnh, bạn phân biệt "lỗi dữ liệu" với "tín hiệu thực" bằng cách nào?
4. Chọn một bài toán phân tích dữ liệu bạn từng gặp và liệt kê 2 giả định rủi ro nhất của mô hình đó.

## Tài liệu tham khảo

- Gelman, A., et al. (2013). *Bayesian Data Analysis*.
- McElreath, R. (2020). *Statistical Rethinking*.

---

*Bài học tiếp theo: [0.21 Mô phỏng để kiểm tra trực giác thống kê]({{ site.baseurl }}/contents/vi/chapter00/00_19_simulation_for_statistical_intuition/)*
