import React, { useState, useEffect } from 'react';

export default function App() {
  const [selectedRole, setSelectedRole] = useState('applicant'); // 'applicant' | 'appraiser'
  const [activeTab, setActiveTab] = useState('action_plan');     // 'action_plan' | 'diff_audit' | 'notice_text'
  const [selectedIssueId, setSelectedIssueId] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [diffReport, setDiffReport] = useState(null);

  // Mẫu dữ liệu các vấn đề vi phạm bóc tách từ công văn kèm tọa độ bản vẽ
  const [issues, setIssues] = useState([
    {
      id: 1,
      issue_number: 1,
      drawing_number: "KT-01",
      drawing_title: "Mặt bằng Tầng 1 (Trệt)",
      issue_description: "Vi phạm khoảng lùi xây dựng phía sau: Thiết kế tường bao sát ranh đất, yêu cầu lùi tối thiểu 1.0m theo quy hoạch.",
      standard_reference: "QCVN 01:2021/BXD Mục 2.6.2",
      discipline: "architecture",
      severity: "critical",
      bounding_box: { x_min: 75, y_min: 15, x_max: 95, y_max: 42 },
      status: "open",
      steps: [
        "Mở bản vẽ KT-01, dịch chuyển toàn bộ tường bao phía sau theo trục Y lùi vào trong 1000mm.",
        "Tính lại mật độ xây dựng và cập nhật Thuyết minh thiết kế."
      ]
    },
    {
      id: 2,
      issue_number: 2,
      drawing_number: "KT-01",
      drawing_title: "Mặt bằng Tầng 1 (Trệt)",
      issue_description: "Cầu thang bộ thoát nạn trục 2-3: Chiều rộng vế thang ghi chú 1.05m là chưa đạt chuẩn, yêu cầu >= 1.20m theo PCCC.",
      standard_reference: "QCVN 06:2022/BXD Mục 3.2.1",
      discipline: "fire_safety",
      severity: "critical",
      bounding_box: { x_min: 38, y_min: 40, x_max: 60, y_max: 68 },
      status: "open",
      steps: [
        "Mở bản vẽ KT-02/KT-03, nới rộng khoảng cách giữa 2 trục tường buồng thang thêm 150mm để thông thủy vế thang đạt 1200mm.",
        "Kiểm tra chiều mở cửa chống cháy theo đúng hướng thoát hiểm ra ngoài."
      ]
    },
    {
      id: 3,
      issue_number: 3,
      drawing_number: "KT-04",
      drawing_title: "Mặt đứng chính trục 1-4",
      issue_description: "Chiều cao tầng 1 đang vẽ 4.2m vượt quá chiều cao quy định cho phép 3.9m theo đồ án quy hoạch chi tiết 1/500.",
      standard_reference: "Quy chế Quản lý Kiến trúc Đô thị",
      discipline: "architecture",
      severity: "major",
      bounding_box: { x_min: 15, y_min: 65, x_max: 40, y_max: 88 },
      status: "open",
      steps: [
        "Hạ cốt dầm sàn Tầng 2 từ +4.200m xuống +3.900m trên bản vẽ Mặt cắt và Mặt đứng chính.",
        "Đồng bộ chiều dài cột tầng 1 sang bản vẽ Kết cấu KC-01."
      ]
    }
  ]);

  const handleRunAI = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setIsAnalyzing(false);
      alert("✅ AI Agent đã hoàn tất bóc tách Công văn & Ánh xạ thành công 3 vị trí vi phạm lên bản vẽ CAD/PDF!");
    }, 1200);
  };

  const handleRunDiff = () => {
    setDiffReport({
      source_version: "V1",
      target_version: "V2 (Nộp lại)",
      resolved_count: 2,
      unresolved_count: 1,
      unauthorized_count: 1,
      resolved_items: [
        "Mục 1 (Khoảng lùi phía sau): Đã lùi 1.0m đạt chuẩn.",
        "Mục 2 (Vế thang thoát hiểm): Đã nới rộng đạt 1.22m."
      ],
      unresolved_items: [
        "Mục 3 (Chiều cao tầng 1): Cốt sàn tầng 2 vẫn đang ghi +4.100m, chưa hạ đủ về +3.900m."
      ],
      unauthorized_warnings: [
        "Phát hiện Ban công Tầng 2 (trục A-C) cơi nới diện tích thêm 1.4m2 ngoài yêu cầu công văn!"
      ]
    });
    setActiveTab('diff_audit');
  };

  const currentIssue = issues.find(i => i.id === selectedIssueId) || issues[0];

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-950 text-slate-100">
      {/* 1. TOP HEADER (TẦNG 1 & TẦNG 2 METRICS) */}
      <header className="h-16 border-b border-slate-800 bg-slate-900/90 px-6 flex items-center justify-between backdrop-blur-md z-30">
        <div className="flex items-center space-x-3">
          <div className="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-lg text-white shadow-lg shadow-blue-500/20">
            DX
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-base tracking-tight text-white">DX-OS Open-Core</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 font-mono border border-blue-500/30">CDE 3-Tier</span>
            </div>
            <p className="text-xs text-slate-400">Nền tảng Thẩm định & Lập Kế hoạch Sửa đổi Hồ sơ Xây dựng</p>
          </div>
        </div>

        {/* CÁC CHỈ SỐ HẠ TẦNG TẦNG 1 */}
        <div className="hidden lg:flex items-center space-x-3 text-xs font-mono">
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/50">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-slate-300">Gateway: APISIX</span>
          </div>
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/50">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span className="text-slate-300">Storage: MinIO S3</span>
          </div>
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/50">
            <span className="w-2 h-2 rounded-full bg-blue-400"></span>
            <span className="text-slate-300">Protocol: MCP Server</span>
          </div>
        </div>

        {/* CHUYỂN ĐỔI VAI TRÒ NGƯỜI DÙNG */}
        <div className="flex items-center space-x-3">
          <div className="bg-slate-800 p-0.5 rounded-lg border border-slate-700 flex text-xs">
            <button
              onClick={() => setSelectedRole('applicant')}
              className={`px-3 py-1.5 rounded-md transition ${selectedRole === 'applicant' ? 'bg-blue-600 text-white font-medium shadow' : 'text-slate-400 hover:text-white'}`}
            >
              👷 Kỹ sư thiết kế
            </button>
            <button
              onClick={() => setSelectedRole('appraiser')}
              className={`px-3 py-1.5 rounded-md transition ${selectedRole === 'appraiser' ? 'bg-purple-600 text-white font-medium shadow' : 'text-slate-400 hover:text-white'}`}
            >
              👨‍💼 Cán bộ thẩm định
            </button>
          </div>
        </div>
      </header>

      {/* 2. BODY CHÍNH CHIA 2 CỘT */}
      <div className="flex flex-1 overflow-hidden">
        {/* CỘT TRÁI: CÔNG VĂN & ACTION PLAN CHECKLIST (40%) */}
        <div className="w-full md:w-5/12 lg:w-4/12 border-r border-slate-800 bg-slate-900/40 flex flex-col h-full overflow-hidden">
          {/* TAB BAR */}
          <div className="p-3 border-b border-slate-800 flex space-x-2 bg-slate-900/60">
            <button
              onClick={() => setActiveTab('action_plan')}
              className={`flex-1 py-1.5 text-xs font-medium rounded transition ${activeTab === 'action_plan' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              📋 Kế hoạch sửa ({issues.length})
            </button>
            <button
              onClick={() => setActiveTab('diff_audit')}
              className={`flex-1 py-1.5 text-xs font-medium rounded transition ${activeTab === 'diff_audit' ? 'bg-purple-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              🔍 Đối soát Diff V1/V2
            </button>
            <button
              onClick={() => setActiveTab('notice_text')}
              className={`flex-1 py-1.5 text-xs font-medium rounded transition ${activeTab === 'notice_text' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              📄 Công văn gốc
            </button>
          </div>

          {/* NỘI DUNG TỪNG TAB */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {activeTab === 'action_plan' && (
              <>
                <div className="bg-slate-800/40 border border-slate-800 rounded-lg p-3">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Hồ sơ: HS-2026-B214</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">Cần sửa đổi (V1)</span>
                  </div>
                  <p className="text-xs text-slate-300">Công văn số 458/SXD-QLĐT yêu cầu hoàn thiện 3 mục kỹ thuật.</p>
                </div>

                <div className="space-y-3">
                  {issues.map((issue) => {
                    const isSelected = issue.id === selectedIssueId;
                    return (
                      <div
                        key={issue.id}
                        onClick={() => setSelectedIssueId(issue.id)}
                        className={`p-3.5 rounded-xl border transition cursor-pointer text-left ${
                          isSelected
                            ? 'bg-blue-950/40 border-blue-500/80 shadow-lg shadow-blue-500/10'
                            : 'bg-slate-900 border-slate-800 hover:border-slate-700'
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-center space-x-2">
                            <span className="w-5 h-5 rounded-full bg-red-500/20 text-red-400 text-xs flex items-center justify-center font-bold">
                              {issue.issue_number}
                            </span>
                            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                              {issue.drawing_number}
                            </span>
                          </div>
                          <span className={`text-[10px] uppercase tracking-wider px-2 py-0.5 rounded font-semibold ${
                            issue.severity === 'critical' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          }`}>
                            {issue.severity}
                          </span>
                        </div>

                        <p className="text-xs text-slate-200 mt-2 font-medium line-clamp-2 leading-relaxed">
                          {issue.issue_description}
                        </p>

                        <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
                          <span className="text-blue-400">📜 {issue.standard_reference}</span>
                          <span className="text-slate-500">Bấm để định vị ➔</span>
                        </div>

                        {isSelected && (
                          <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-2">
                            <span className="text-[11px] font-semibold text-emerald-400 block">
                              🛠️ Các bước hành động đề xuất (Action Plan):
                            </span>
                            {issue.steps.map((st, idx) => (
                              <div key={idx} className="flex items-start space-x-2 text-xs text-slate-300 bg-slate-950/50 p-2 rounded border border-slate-800/60">
                                <span className="text-emerald-400 font-bold">✓</span>
                                <span className="leading-snug">{st}</span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </>
            )}

            {activeTab === 'diff_audit' && (
              <div className="space-y-4">
                <div className="bg-purple-950/30 border border-purple-800/50 rounded-xl p-3.5">
                  <h4 className="text-sm font-bold text-purple-300 flex items-center space-x-2">
                    <span>🔍 Báo cáo Đối soát Sai lệch Tự động</span>
                  </h4>
                  <p className="text-xs text-slate-300 mt-1">So sánh bản vẽ ban đầu (V1) với bản vẽ nộp lại (V2) của Kỹ sư.</p>
                  
                  {!diffReport ? (
                    <button
                      onClick={handleRunDiff}
                      className="mt-3 w-full py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold shadow-lg transition"
                    >
                      🚀 Chạy Đối soát Phiên bản V1 vs V2 ngay
                    </button>
                  ) : (
                    <div className="mt-3 space-y-3">
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div className="p-2 rounded bg-emerald-950/40 border border-emerald-800/50">
                          <span className="text-lg font-bold text-emerald-400 block">{diffReport.resolved_count}</span>
                          <span className="text-[10px] text-slate-400">Đã sửa đạt</span>
                        </div>
                        <div className="p-2 rounded bg-red-950/40 border border-red-800/50">
                          <span className="text-lg font-bold text-red-400 block">{diffReport.unresolved_count}</span>
                          <span className="text-[10px] text-slate-400">Chưa sửa đạt</span>
                        </div>
                        <div className="p-2 rounded bg-amber-950/40 border border-amber-800/50">
                          <span className="text-lg font-bold text-amber-400 block">{diffReport.unauthorized_count}</span>
                          <span className="text-[10px] text-slate-400">Cảnh báo sửa lén</span>
                        </div>
                      </div>

                      <div className="space-y-2 text-xs">
                        <span className="font-semibold text-emerald-400 block">✓ Đã khắc phục hợp lệ:</span>
                        {diffReport.resolved_items.map((r, i) => (
                          <div key={i} className="p-2 bg-emerald-950/20 border border-emerald-900/50 rounded text-slate-300">
                            {r}
                          </div>
                        ))}

                        <span className="font-semibold text-red-400 block pt-1">✗ Chưa đạt (Cần yêu cầu nộp lại):</span>
                        {diffReport.unresolved_items.map((ur, i) => (
                          <div key={i} className="p-2 bg-red-950/20 border border-red-900/50 rounded text-slate-300">
                            {ur}
                          </div>
                        ))}

                        <span className="font-semibold text-amber-400 block pt-1">⚠️ Cảnh báo thay đổi ngoài yêu cầu:</span>
                        {diffReport.unauthorized_warnings.map((w, i) => (
                          <div key={i} className="p-2 bg-amber-950/20 border border-amber-900/50 rounded text-amber-200">
                            {w}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'notice_text' && (
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono leading-relaxed space-y-2">
                <p className="text-amber-400 font-bold">CÔNG VĂN SỐ: 458/SXD-QLĐT</p>
                <p>Kính gửi: Công ty TNHH Tư vấn & Phát triển Đô thị</p>
                <p>1. Mặt bằng Tầng 1 (KT-01): Vi phạm khoảng lùi phía sau sát ranh đất, yêu cầu lùi 1.0m theo QCVN 01:2021.</p>
                <p>2. Buồng thang thoát hiểm trục 2-3 (KT-01): Bề rộng bản thang 1.05m là chưa đạt chuẩn, yêu cầu >= 1.20m theo QCVN 06:2022.</p>
                <p>3. Mặt đứng chính (KT-04): Chiều cao tầng 1 đang vẽ 4.2m vượt quá chiều cao cho phép 3.9m.</p>
              </div>
            )}
          </div>

          {/* ACTION FOOTER */}
          <div className="p-3 border-t border-slate-800 bg-slate-900/80 flex space-x-2">
            <button
              onClick={handleRunAI}
              disabled={isAnalyzing}
              className="flex-1 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white rounded-lg text-xs font-semibold shadow-md transition flex items-center justify-center space-x-1"
            >
              <span>{isAnalyzing ? "⏳ AI đang bóc tách..." : "⚡ Chạy AI Thẩm định lại"}</span>
            </button>
            <button
              onClick={() => alert("📄 Đã xuất file Báo cáo Giải trình (.docx) thành công để Kỹ sư ký và nộp kèm!")}
              className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 transition"
            >
              📥 Xuất File Giải trình
            </button>
          </div>
        </div>

        {/* CỘT PHẢI: TRÌNH XEM BẢN VẼ TƯƠNG TÁC (INTERACTIVE BLUEPRINT VIEWER) (60%) */}
        <div className="flex-1 bg-slate-950 flex flex-col h-full relative overflow-hidden">
          {/* TOOLBAR BẢN VẼ */}
          <div className="h-12 border-b border-slate-800 bg-slate-900/60 px-4 flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-slate-200">📐 Bản vẽ: {currentIssue.drawing_number} - {currentIssue.drawing_title}</span>
              <span className="text-slate-500">|</span>
              <span className="text-slate-400">Tỷ lệ: 1/100 • Khổ A1 Vector</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-[10px] font-mono">OpenBIM Renderer</span>
              <button
                onClick={() => alert("Zoom 100%")}
                className="px-2 py-1 rounded bg-slate-800 text-slate-300 hover:bg-slate-700"
              >
                🔍 100%
              </button>
            </div>
          </div>

          {/* VÙNG CANVAS HIỂN THỊ BẢN VẼ KỸ THUẬT */}
          <div className="flex-1 p-6 flex items-center justify-center overflow-auto bg-slate-950/90 relative">
            <div className="relative w-full max-w-4xl aspect-[1.414] bg-slate-900 rounded-lg shadow-2xl border border-slate-800 p-8 flex flex-col justify-between overflow-hidden">
              
              {/* LƯỚI TRỤC TỌA ĐỘ VÀ NÉT VẼ CAD GIẢ LẬP (SVG VECTOR LAYER) */}
              <svg className="absolute inset-0 w-full h-full stroke-slate-800/80" strokeWidth="1">
                {/* Lưới trục tọa độ */}
                <line x1="10%" y1="0" x2="10%" y2="100%" strokeDasharray="4 4" />
                <line x1="35%" y1="0" x2="35%" y2="100%" strokeDasharray="4 4" />
                <line x1="65%" y1="0" x2="65%" y2="100%" strokeDasharray="4 4" />
                <line x1="90%" y1="0" x2="90%" y2="100%" strokeDasharray="4 4" />
                
                <line x1="0" y1="20%" x2="100%" y2="20%" strokeDasharray="4 4" />
                <line x1="0" y1="50%" x2="100%" y2="50%" strokeDasharray="4 4" />
                <line x1="0" y1="80%" x2="100%" y2="80%" strokeDasharray="4 4" />
              </svg>

              {/* TƯỜNG BAO & PHÒNG ỐC NỘI BỘ */}
              <div className="relative z-10 w-full h-full border-2 border-slate-600/70 p-4 flex flex-col justify-between">
                
                {/* KHU VỰC PHÍA SAU (RANH ĐẤT & KHOẢNG LÙI) */}
                <div className="h-24 border-b border-dashed border-slate-700 flex items-center justify-between px-6 text-slate-500 text-xs">
                  <span>RANH GIỚI ĐẤT PHÍA SAU</span>
                  <span className="font-mono text-red-400/80">KHOẢNG LÙI HIỆN TẠI: 0.0M (YÊU CẦU >= 1.0M)</span>
                </div>

                {/* KHU VỰC TRUNG TÂM (BUỒNG THANG & SẢNH CHÍNH) */}
                <div className="flex-1 grid grid-cols-3 gap-4 p-4 text-xs text-slate-400">
                  <div className="border border-slate-700/60 p-3 rounded bg-slate-950/40 flex flex-col justify-between">
                    <span className="font-semibold text-slate-300">PHÒNG KHÁCH</span>
                    <span className="font-mono text-[10px] text-slate-500">S = 28.5 m²</span>
                  </div>
                  <div className="border border-slate-700/60 p-3 rounded bg-slate-950/40 flex flex-col justify-between">
                    <span className="font-semibold text-slate-300">BUỒNG THANG BỘ</span>
                    <span className="font-mono text-[10px] text-amber-400">BẢN THANG: 1050 mm (THIẾU 150mm)</span>
                  </div>
                  <div className="border border-slate-700/60 p-3 rounded bg-slate-950/40 flex flex-col justify-between">
                    <span className="font-semibold text-slate-300">BẾP & ĂN</span>
                    <span className="font-mono text-[10px] text-slate-500">S = 22.0 m²</span>
                  </div>
                </div>

                {/* KHUNG TÊN BẢN VẼ TIÊU CHUẨN (TITLE BLOCK) */}
                <div className="h-16 border-t border-slate-700 flex items-center justify-between px-4 text-[11px] text-slate-400 bg-slate-950/60">
                  <div>
                    <span className="block font-bold text-slate-300">CÔNG TRÌNH: NHÀ Ở KẾT HỢP VĂN PHÒNG</span>
                    <span>ĐỊA ĐIỂM: LÔ B2-14 KHU ĐÔ THỊ MỚI</span>
                  </div>
                  <div className="text-right font-mono">
                    <span className="block font-bold text-blue-400">BẢN VẼ SỐ: {currentIssue.drawing_number}</span>
                    <span>TỶ LỆ: 1/100</span>
                  </div>
                </div>
              </div>

              {/* BOUNDING BOX HIGHLIGHT CỦA TỪNG VẤN ĐỀ TRÊN BẢN VẼ */}
              {issues.map((iss) => {
                const isSelected = iss.id === selectedIssueId;
                const { x_min, y_min, x_max, y_max } = iss.bounding_box;
                return (
                  <div
                    key={iss.id}
                    onClick={() => setSelectedIssueId(iss.id)}
                    style={{
                      left: `${x_min}%`,
                      top: `${y_min}%`,
                      width: `${x_max - x_min}%`,
                      height: `${y_max - y_min}%`,
                    }}
                    className={`absolute z-20 rounded border-2 transition-all cursor-pointer flex flex-col justify-between p-1.5 ${
                      isSelected
                        ? 'border-red-500 bg-red-500/20 shadow-2xl shadow-red-500/50 ring-4 ring-red-500/30'
                        : 'border-red-500/60 bg-red-500/10 hover:border-red-400'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="px-1.5 py-0.5 rounded bg-red-600 text-white font-bold text-[10px] shadow">
                        Lỗi #{iss.issue_number}
                      </span>
                      {isSelected && (
                        <span className="animate-ping w-2 h-2 rounded-full bg-red-400"></span>
                      )}
                    </div>
                    <span className="text-[10px] bg-slate-950/90 text-red-300 px-1 py-0.5 rounded font-mono truncate">
                      {iss.standard_reference}
                    </span>
                  </div>
                );
              })}

            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
