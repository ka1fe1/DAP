-- change log
-- 20017-06-08 Harriet 
-- 1. extract the number and % from name and move to spec
-- 2. extract the dosage form from name  and move to dosage form  (**） 
-- 2017-09-09 harriet
--  remove unimportant words from the name 

-- back log
 
-- handle  the 厂家信息 in the name,  (1) l_company_en_name  拆分 国家 和 厂名  （2） 本脚本中仿照 df 的处理 方式，将 厂家信息 移到 compangy 
-- spec remove unnessary chinese and chemical formular


SET FOREIGN_KEY_CHECKS = 0;

set @OR_OP = '||';
set @AND_OP = '&&';
set @OR_OP_M = concat('%',@OR_OP,'%');
set @AND_OP_M = concat('%',@AND_OP,'%');
set @OR_AND_SEP = '||&&';  --  the beginnig of AND groups
set @OR_AND_SEP_M = '%||&&%';  --  the beginnig of AND groups
  
set @INVALID_SCORE = -1;

-- todo:

--  set @CASE_CD = 'nx';  -- benchmark 
--   set @CASE_CD = 'nx-s';  -- test usually we only work on this case
--  set @CASE_CD = 'hdf_7000';
-- set @CASE_CD = 'hdf_7000_t';
-- set @CASE_CD =  'hdf_10000';
--  set @CASE_CD =  'hdf_7000_0614';
-- set @CASE_CD = 'nx-p-a'; -- BENCHMARK
-- set @CASE_CD = 'nx-p-a-1'; -- TEST
--  set @CASE_CD =  'cc_v2';
 set @CASE_CD =  'single';
--  set @CASE_CD =  'hdf_web_t';


-- select * from case_dcm;
update case_dcm set state = 'p' where state='w';  -- in future handling waiting 
update case_dcm set state = 'w' where cd = @CASE_CD;

select id into @CASE_ID from case_dcm where state = 'w';
-- select * from case_dcm_data where case_id in (14,17) order by id_s;     

-- select * from case_dcm where state = 'w';

drop table if exists dcm_data_wip;

CREATE TABLE `dcm_data_wip` (     -- 111 for lite check
  `id` int(11) unsigned NOT NULL,
   bj_id int unsigned default null,
  `score` smallint default 0,
  `an_raw` varchar(500) DEFAULT '',
-- an_shrt_srch varchar(255) DEFAULT '',   
   an_srch varchar(500) DEFAULT '',   
   an_srch_id int unsigned DEFAULT null,   
  `name_raw` varchar(255) DEFAULT '',
--  name_shrt_srch varchar(255) DEFAULT '',   
   name_srch varchar(255) DEFAULT '',   
   name_srch_id int unsigned DEFAULT null,   
  `df_raw` varchar(255) DEFAULT '',
--   df_shrt_srch varchar(255) DEFAULT '',   
   df_srch varchar(255) DEFAULT '',   
   df_srch_id int unsigned DEFAULT null,   
  `spec_raw` varchar(700) DEFAULT '',
--  spec_shrt_srch varchar(500) DEFAULT '',   
   spec_srch varchar(500) DEFAULT '',   
   spec_srch_id int unsigned DEFAULT null,   
  `company_raw` varchar(255) DEFAULT '',
--   company_shrt_srch varchar(255) DEFAULT '',   
   company_srch varchar(255) DEFAULT '',   
   company_srch_id int unsigned DEFAULT null,
   name_srched tinyint unsigned default 0,
   company_srched tinyint unsigned default 0,
   name_score smallint default 0,
   company_score smallint default 0,
   name_m_srch_id int unsigned DEFAULT null,
   company_m_srch_id int unsigned DEFAULT null,
   key (an_srch_id),  
   key (score),  
   key (name_srch_id),  
   key (df_srch_id),  
   key (spec_srch_id),  
   key (company_srch_id),
   key (company_srched),
   key (name_srched),
   PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `dcm_data_wip`
(id, 
`an_raw`,
name_raw,
`df_raw`,
`spec_raw`,
`company_raw`)
SELECT distinct
   w.id_s,
    w.an_s AS an_raw,
     w.`name_s` AS name_raw,
     w.df_s as df_raw,
     w.`spec_s` AS spec_raw,
    w.`company_s` AS company_raw
    FROM
    case_dcm_data w 
--  , wip_dcm_res_diff d
WHERE
  w.case_id =   @CASE_ID
  -- and (!(df_s = '中草药' and an_s is null)) 
   -- and w.id_s = d.id_s
    order by id_s  
--  limit 100  
   ;
   

-- select * from dcm_data_wip d where  d.an_raw in ('国药准字H51021158','H20130603'); 

-- sigle dcm: java, prepare dcm_dat_wip 


drop table if exists dcm_srch_str_term;

CREATE TABLE dcm_srch_str_term (
  `str` varchar(600) default '',
  `srch_str` varchar(600) default '',
  `type` char(1) NOT NULL DEFAULT '',
   KEY `srch_str` (`srch_str`),
  KEY `type` (`type`),
  PRIMARY KEY `tsype` (`str`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists dcm_srch_term;

CREATE TABLE dcm_srch_term (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `srch_str` varchar(700) default '',
  `srch_shrt_str` varchar(700) default '',
  `type` char(1) NOT NULL DEFAULT '',
   KEY `srch_str` (`srch_str`),
  KEY `type` (`type`),
  unique KEY `tsype` (`srch_str`,`type`),
  PRIMARY KEY (`id`)
) AUTO_INCREMENT=1000 ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists dcm_srch_x_data;
 
CREATE TABLE `dcm_srch_x_data` (
  `data_id` int(11) unsigned NOT NULL,
  `srch_id` int(11) unsigned NOT NULL,
  `srch_str` varchar(500) default '',
  `type` char(1) NOT NULL DEFAULT '',
   KEY `srch_str` (`srch_str`),
   KEY `type` (`type`),
  PRIMARY KEY (data_id,srch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



INSERT INTO dcm_srch_str_term  -- 507
(`str`,
`type`) 
select distinct name_raw as str, 'n' as type
from dcm_data_wip where name_raw is not null
union 
select distinct spec_raw as str, 's' as type
from dcm_data_wip where spec_raw is not null
union
select distinct company_raw as str, 'c' as type
from dcm_data_wip where company_raw is not null
union 
select distinct an_raw as str, 'a' as type 
from dcm_data_wip where an_raw is not null
union
select distinct df_raw as str, 'd' as type 
from dcm_data_wip where df_raw is not null
;

-- 通用数据转换 

update dcm_srch_str_term set srch_str = trim(lower(str));
update dcm_srch_str_term set srch_str  = trim(translate_alias(srch_str,'w'));
update dcm_srch_str_term set srch_str = replace(srch_str,'\"','') where srch_str like '%\"%';

-- 清理HTML tag
update dcm_srch_str_term set srch_str = replace (srch_str,'<','< ') where srch_str regexp '<';
update dcm_srch_str_term set srch_str = replace (srch_str,'>',' >') where srch_str regexp '>';
-- select * from dcm_srch_str_term  where srch_str like '%<%';  -- 清理HTML tag
-- select * from dcm_srch_str_term  where srch_str like '%<%' and srch_str not in (select distinct srch_str from dcm_srch_str_term  where srch_str regexp '[<].+[span|sup|div|img|u|b].+[>]');

update dcm_srch_str_term set srch_str =  replace_seg_by_regexp (srch_str ,  '<', '>',  ' ','[<].+[span|sup|div|img|u|b].+[>]') where srch_str regexp '[<].+[span|sup|div|img|u|b].+[>]'; -- html tag
-- select * from dcm_srch_str_term  where str like '%<%';

update dcm_srch_str_term set srch_str = replace(srch_str,'null','无') where concat(' ',srch_str,' ') regexp '[^a-zA-Z]null[^a-zA-Z]'; 

update dcm_srch_str_term set srch_str = remove_duplicate_seg(@OR_OP, srch_str,0) where srch_str like @OR_OP_M;
update dcm_srch_str_term set srch_str = remove_duplicate_seg(@AND_OP, srch_str,0) where srch_str like @AND_OP_M;

-- select * from dcm_srch_str_term where concat(' ',srch_str,' ') regexp '[^a-zA-Z]null[^a-zA-Z]';
delete from dcm_srch_str_term where srch_str = '' or srch_str is null; 
update dcm_srch_str_term set srch_str  = replace (srch_str, '  ',' ');

update dcm_data_wip m inner join dcm_srch_str_term s on m.spec_raw = s.str and s.type = 's' set m.spec_srch = s.srch_str;
update dcm_data_wip m inner join dcm_srch_str_term s on m.df_raw = s.str and s.type = 'd' set m.df_srch = s.srch_str;

-- select * from dcm_srch_str_term where type ='a'

-- **** 处理approval no 
drop table if exists wip_str_trans;
create table wip_str_trans -- 1838
as 
select distinct srch_str as origin, srch_str as str_raw, srch_str as str_new ,  srch_str as seg_new,  srch_str as seg_ret
from dcm_srch_str_term where type ='a' and str <>'';

ALTER TABLE wip_str_trans ADD  INDEX  (`origin` );
ALTER TABLE wip_str_trans ADD  INDEX  (`str_raw` );
ALTER TABLE wip_str_trans ADD  INDEX  (`str_new` );

call extractApprovalNo();

-- select * from wip_str_trans where str_raw <> str_new order by origin;
-- update wip_str_trans  set str_raw =   str_new  ; -- 56
-- update wip_str_trans  set str_new =   str_raw  ; -- 56

  
update dcm_srch_str_term w inner join wip_str_trans t on w.type ='a' and w.srch_str = t.origin  set w.srch_str = t.str_new ; -- 964
-- todo select * from dcm_srch_str_term w where str= srch_str and type ='a';
-- select t.str_new, t.origin, w.* from dcm_srch_str_term w inner join wip_str_trans t on w.type ='a' and w.srch_str = t.origin;


-- **** 处理药名 process name 


-- select right(srch_str,INSTR(srch_str,'(')),  d.* from dcm_srch_str_term d where type ='n' and srch_str like '%(%)%';

-- update dcm_srch_str_term set srch_str = LEFT(srch_str,INSTR(srch_str,'(')-1) where type = 'n' and srch_str like '%(%)%' ;
-- update dcm_srch_str_term set srch_str = substring(srch_str, 1, char_length(srch_str)-1) where type = 'n' and srch_str like  '%t';
-- update dcm_srch_str_term set srch_str= translate_alias(srch_str,'n') where type = 'n';

drop table if exists wip_str_trans;
create table wip_str_trans -- 1838
as 
select distinct str as origin, srch_str as str_raw, srch_str as str_new ,  srch_str as seg_new,  srch_str as seg_ret
from dcm_srch_str_term where type ='n' and srch_str <>''; -- 必须用 str as origin

ALTER TABLE wip_str_trans ADD  INDEX  (`origin` );
ALTER TABLE wip_str_trans ADD  INDEX  (`str_raw` );
ALTER TABLE wip_str_trans ADD  INDEX  (`str_new` );

update wip_str_trans  set seg_ret='', seg_new = '';


-- select name_raw, concat(LEFT(name_raw,INSTR(name_raw,'(')-1),substring(name_raw,INSTR(name_raw,')')+1)) from dcm_data_wip where name_raw like '%(%)%';
-- to do better to keep the bracket
-- update wip_str_trans  set str_new = concat(LEFT(str_new,INSTR(str_new,'(')-1),substring(str_new,INSTR(str_new,')')+1)) where str_new like '%(%)%' ;  -- remove ()
update wip_str_trans  set str_new = substring(str_new, 1, char_length(str_new)-1) where str_new like  '%t';

-- extract the number and % from name and move to spec
-- select * from wip_str_trans  where str_new regexp '[0-9]%';
update wip_str_trans set seg_ret = get_percent_seg(str_new) where str_new regexp '[0-9]%';
-- select get_percent_seg("0.9%氯化钠注射液");
update wip_str_trans set str_new = replace(str_new, seg_ret,'') where seg_ret <>'';

update dcm_data_wip set spec_raw = '' where spec_raw is null;
update dcm_data_wip m inner join wip_str_trans s on m.name_raw = s.origin and s.seg_ret <>''  and m.spec_raw not like concat('%',s.seg_ret,'%')
	set m.spec_raw = 
    case when m.spec_raw ='' then s.seg_ret else concat(s.seg_ret,@AND_OP,m.spec_raw) end,
    m.spec_srch = case when m.spec_srch = '' then s.seg_ret else concat(s.seg_ret,@AND_OP,m.spec_srch) end;
-- select concat(s.seg_ret,@AND_OP,m.spec_raw), concat(s.seg_ret,@AND_OP,m.spec_srch) , m.* 
-- from dcm_data_wip m inner join wip_str_trans s on m.name_raw = s.origin  and s.seg_ret <>''  and m.spec_raw not like concat('%',s.seg_ret,'%');

replace into dcm_srch_str_term  
(`str`, `srch_str`,`type`) 
select distinct spec_raw as str, spec_srch,'s' as type
from dcm_data_wip;
--  where spec_raw like  @AND_OP_M;


-- 
update wip_str_trans  set str_new =  translate_alias(str_new,'n');
call cleanStrExtraDelims();
call cleanStrExtraDelim(@OR_OP,1);

call translateDrugName();  -- 2017-10-31 


-- clean extra numbers
update wip_str_trans  set str_new = clean_char(str_new,' ','n');
call cleanStrExtraDelim(' ',0);
call cleanStrExtraDelim('()',0);




-- select * from wip_str_trans where origin regexp '-谷氨酰胺注射液';

-- select max(char_length(str_new)) from wip_str_trans where str_new regexp '[0-9]';
update wip_str_trans w inner join l_drug_name_and t on w.str_new like concat('%',t.name,'%')   -- 5801
set w.str_new = replace(w.str_new,t.name, t.name_new);

update wip_str_trans set str_new = move_andseg_to_end(str_new);
update wip_str_trans  set str_new =  remove_duplicate_seg(@OR_OP,str_new,0);

call removeDrugNameFix();  -- 867
update  wip_str_trans w set str_new =seg_new where seg_new <>'' and char_length(seg_new)>1;  -- 至少要2个字,否则匹配太宽泛
-- select * from wip_str_trans where origin regexp '辛伐他汀胶囊';


-- extract the dosage form from name  and move to dosage form  (**） 
 
update dcm_data_wip set df_raw = '' where df_raw is null;
update dcm_data_wip m inner join wip_str_trans s on m.name_raw = s.origin and s.seg_ret <>''  and m.df_raw not like concat('%',s.seg_ret,'%')
	set m.df_raw = case when m.df_raw = '' then s.seg_ret else  concat(s.seg_ret,@OR_OP,m.df_raw) end, 
	 m.df_srch = case when m.df_srch ='' then s.seg_ret else concat(s.seg_ret,@OR_OP,m.df_srch) end;

--  select concat(s.seg_ret,@OR_OP,m.df_raw),  concat(s.seg_ret,@OR_OP,m.df_srch), m.* 
--  from dcm_data_wip m inner join wip_str_trans s on m.name_raw = s.origin  and s.seg_ret <>'' and m.df_raw not like concat('%',s.seg_ret,'%')

replace into dcm_srch_str_term  
(`str`, `srch_str`,`type`) 
select distinct df_raw as str,  df_srch, 'd' as type
from dcm_data_wip;

-- update wip_str_trans  set str_new =   str_raw  ; -- 56

--  remove unimportant words in the name 

update wip_str_trans  set str_new = replace(str_new, '(',' ');
update wip_str_trans  set str_new = replace(str_new, ')',' ');

-- update wip_str_trans  set str_raw =   str_new  ; -- 56


-- select * from wip_str_trans where trim(str_raw) <> trim(str_new) order by origin;

-- select count(b.word) into n from wip_str_trans w inner join l_unimportant_word b on b.w= i and b.s
-- TODO: run data set a of zx 时，卡住跑不动了, 故先注释掉
call removeUnimportantWord('n');


update dcm_srch_str_term w inner join wip_str_trans t on w.type ='n' and w.str = t.origin  set w.srch_str = t.str_new; -- 964
-- select w.srch_str = t.str_new, w.str = t.origin, w.srch_str, t.str_new, w.*, t.* from dcm_srch_str_term w inner join wip_str_trans t on w.str = t.origin  and w.type ='n';

  
-- select * from dcm_srch_str_term where type ='n' and srch_str != str;
-- select * from dcm_srch_str_term where type ='d' and srch_str != str;

-- 处理剂型 process df 

update dcm_srch_str_term set srch_str = clean_char(srch_str,'','n') where type = 'd' ; -- 15
update dcm_srch_str_term set srch_str = translate_alias(srch_str,'d') where type = 'd' ; -- 15
-- select * from b_alias where scope ='d';
update dcm_srch_str_term set srch_str = replace(srch_str,'制剂','') where type = 'd'; 
update dcm_srch_str_term set srch_str = replace(srch_str,'剂型','') where type = 'd'; 
update dcm_srch_str_term set srch_str = replace(srch_str,'剂','') where type = 'd'; 

-- select * from dcm_srch_str_term where type='c' order by char_length(srch_str) desc 
-- select * from dcm_srch_str_term where type ='d' and srch_str != str;

-- 处理规格 process spec 

drop table if exists wip_str_trans;
create table wip_str_trans -- 1838
as 
select distinct w.srch_str as origin, w.srch_str as str_raw, w.srch_str as str_new ,  w.srch_str as seg_new,  w.srch_str as seg_ret
from dcm_srch_str_term w where srch_str <>'' and type='s';
ALTER TABLE wip_str_trans ADD unique INDEX  (`origin` );
ALTER TABLE wip_str_trans ADD  INDEX  (`str_raw` );
ALTER TABLE wip_str_trans ADD  INDEX  (`str_new` );
alter table wip_str_trans change column `str_new` `str_new` varchar(1000) default '';
alter table wip_str_trans change column `str_raw` `str_raw` varchar(1000) default '';

-- update wip_str_trans  set str_new =  translate_alias(origin,'w');
update wip_str_trans  set seg_new='',seg_ret='';

update wip_str_trans  set str_new = replace_string_by_regexp(str_new,' ',@OR_OP,'[0-9] [0-9]') where str_new regexp '[0-9] [0-9]'; -- seperate the numbers

call cleanStrExtraDelim(' ',0);
call cleanStrExtraDelim('--',0);

update wip_str_trans  set str_new =  replace_seg_by_regexp (str_new, '(', ')', @OR_OP,'[(][0-9 ]+[)]') where str_new regexp '[(][0-9 ]+[)]'; -- 清除纯数字括号 
-- update wip_str_trans  set str_new =  replace_seg_by_regexp (str_new,  '(', ')',  @OR_OP,'[(][a-zA-Z ]+[)]') where str_new regexp '[(][a-zA-Z ]+[)]'; -- 清除纯字母括号 
update wip_str_trans  set str_new =  replace_seg_by_regexp (str_new,  '(', ')',  @OR_OP,'[(][ivabcde ]+[)]') where str_new regexp '[(][ivabcde ]+[)]'; -- 清除纯字母括号 
-- update wip_str_trans  set str_new =  replace_seg_by_regexp (str_new,  '(', ')',  @OR_OP,'[(][a-zA-Z ]+[)]') where str_new regexp '[<][^0-9mla-zA-Z ]+[>]'; -- html tag
update wip_str_trans  set str_new =  translate_alias(str_new,'s');

-- todo clean (1) 1.6g(c15h16n2o6s2 1.5g与c8h9no5 0.1g);(2)3.2g(c15h16n2o6s2 3.0g与c8h9no5 0.2g).  '(1)0.45g (c18h33cln2o5s计算)'

update wip_str_trans  set str_new = replace(str_new, '-;||','');
update wip_str_trans  set str_new = replace(str_new, '||.','||');
update wip_str_trans  set str_new = replace(str_new, '||,','||');
update wip_str_trans  set str_new = replace(str_new, ';||','||');

update wip_str_trans  set str_new = '' where str_new ='-';
update wip_str_trans  set str_new =  replace(str_new, concat('.',@OR_OP),@OR_OP);
update wip_str_trans  set str_new =  replace(str_new,concat('-',@OR_OP),@OR_OP);

-- select * from wip_str_trans where str_new regexp '<'; 

call cleanStrExtraDelim(@OR_OP,1);

update wip_str_trans  set str_new = replace_seg(str_new, '按', '计','') where str_new like concat('%','按','%', '计','%');
update wip_str_trans  set str_new = replace_seg(str_new, '以', '计','') where str_new like concat('%','以','%', '计','%');

-- todo: 清理纯字母括号，清理b1, b6 字母+数字

update wip_str_trans  set str_new = remove_duplicate_seg(@OR_OP,str_new,1) where str_new like @OR_OP_M;  -- match exact

-- select * from wip_str_trans where str_raw <> str_new order by origin;

-- update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'gug','ug','[0-9]gug[^a-z]')  where str_raw regexp '[0-9]gug[^a-z]' ; -- seperate the numbers
-- update wip_str_trans  set str_new = translate_alias(str_new,'s'); -- 158234 163.86s 157403  104s


-- select * from wip_str_trans where origin regexp '([0-9]+\\.[0-9]+mg|[0-9]+mg).*(与|;).*([0-9]+\\.[0-9]+mg|[0-9]+mg).*' ;

update wip_str_trans  set str_new = concat(' ', str_new,' ');

update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'gug','ug','[0-9]gug[^a-z]')  where str_raw regexp '[0-9]gug[^a-z]' ; -- seperate the numbers
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'mgg','mg','[0-9]mgg[^a-z]') where str_new regexp '[0-9]mgg[^a-z]';
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'mlml','ml','[0-9]mlml[^a-z]') where str_new regexp '[0-9]mlml[^a-z]' ;

update wip_str_trans  set str_new = convert_measure_unit(str_new);  -- 


update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'gug','ug','[0-9]gug[^a-z]')  where str_raw regexp '[0-9]gug[^a-z]' ; -- seperate the numbers
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'mgg','mg','[0-9]mgg[^a-z]') where str_new regexp '[0-9]mgg[^a-z]';
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'mlml','ml','[0-9]mlml[^a-z]') where str_new regexp '[0-9]mlml[^a-z]' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'cm2','cm','[0-9][x][.0-9]+cm2') where str_new regexp '[0-9][x][.0-9]+cm2';
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'x','cm x ','[0-9][x][.0-9]+cm') where str_new regexp '[0-9][x][.0-9]+cm';
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','mgbq ','[0-9][\-][.0-9]+mgbq') where str_new regexp '[0-9][\-][.0-9]+mgbq' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','% ','[0-9][\-][.0-9]+[%]') where str_new regexp '[0-9][\-][.0-9]+[%]' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','mci ','[0-9][\-][.0-9]+mci') where str_new regexp '[0-9][\-][.0-9]+mci' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','mbq ','[0-9][\-][.0-9]+mbq') where str_new regexp '[0-9][\-][.0-9]+mbq' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','ml ','[0-9][\-][.0-9]+ml') where str_new regexp '[0-9][\-][.0-9]+ml' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','mm ','[0-9][\-][.0-9]+mm') where str_new regexp '[0-9][\-][.0-9]+mm' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','mg ','[0-9][\-][.0-9]+mg') where str_new regexp '[0-9][\-][.0-9]+mg' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','kg ','[0-9][\-][.0-9]+kg') where str_new regexp '[0-9][\-][.0-9]+kg' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','剂 ','[0-9][\-][.0-9]+剂') where str_new regexp '[0-9][\-][.0-9]+剂' ;
update wip_str_trans  set str_new = replace_string_by_regexp(str_new,'-','包 ','[0-9][\-][.0-9]+包') where str_new regexp '[0-9][\-][.0-9]+包' ;

update wip_str_trans  set str_new =  replace (str_new, '每',' ');

update wip_str_trans  set str_new = seperate_char(str_new, @AND_OP, 'cen');
-- update dcm_srch_str_term set srch_str =  replace(srch_str,'*g','*') where  type = 's' and srch_str like '*g'; -- 33
-- update dcm_srch_str_term set srch_str =  replace(srch_str,':','*') where  type = 's' and srch_str like '%:%'; -- 33
-- update dcm_srch_str_term set srch_str =  replace(srch_str,'*',@AND_OP) where type = 's' and srch_str like '%*%';  -- 81
-- update dcm_srch_str_term set srch_str =  replace(srch_str,'(',@AND_OP) where type = 's' and srch_str like '%(%';  -- 81
-- update dcm_srch_str_term set srch_str =  replace(srch_str,')',@AND_OP) where type = 's' and srch_str like '%)%';  -- 81
-- update dcm_srch_str_term set srch_str =  replace (srch_str,'/',@AND_OP) where type = 's' and srch_str like '%/%';  -- 17
-- update dcm_srch_str_term set srch_str =  replace (srch_str,' ',@AND_OP) where type = 's' and srch_str like '% %';  -- 1

update wip_str_trans  set str_new =  replace (str_new,' i','');  -- 17

call cleanStrExtraDelim(' ',0);


-- select * from nx_wip where spec ='1.5万博来霉素单位'


-- start with number then match target shouldn't have any other numbers
-- 1. 头： '[^.0-9]'
-- 2. '&&剂'：'[^.0-9igmul]'
-- 3. '&&包'：'[^.0-9igmul]'
-- 4. &&： '[^.0-9]&&[^.0-9]'
-- 5. 尾，结尾是以数字结尾，尾巴加上 '[^.0-9]'


update wip_str_trans  set str_new = replace(str_new,'-;','');
update wip_str_trans  set str_new = replace(str_new,':-;','');
update wip_str_trans  set str_new = replace(str_new,':-','');


update wip_str_trans  set str_new =  replace (str_new,'&&剂','[^.0-9igmul]&&');  -- 把需要的中文 进行转换 
update wip_str_trans  set str_new =  replace (str_new,'&&包','[^.0-9igmul]&&');  -- 把需要的中文 进行转换 

-- except 剂 包, clean up other 中文

update wip_str_trans  set str_new = clean_char(str_new,'','c');



update wip_str_trans  set str_new = remove_duplicate_seg(@AND_OP,str_new,1) where str_new like @AND_OP_M;  -- match exact


--  update wip_str_trans  set str_raw =  str_new  ; 
-- update wip_str_trans  set str_new =  str_raw  ; 
-- select * from wip_str_trans where str_raw <> str_new order by origin limit 0, 2000;


-- select * from wip_str_trans where str_new regexp '^[0-9]';
update wip_str_trans  set str_new =  concat('[^.0-9]', str_new) where  str_new regexp '^[0-9]';  -- 如果是数字开头，加限定不予许被匹配的字符有额外数字

update wip_str_trans  set str_new =  replace (str_new,'&&','&&[^.0-9]') ;

update wip_str_trans  set str_new =   concat(str_new,'[^.0-9]') where str_new regexp '[0-9]$';  -- 88

call cleanStrExtraDelim(' ',0);
update wip_str_trans  set str_new = remove_duplicate_seg(@AND_OP,str_new,1) where str_new like @AND_OP_M;
-- select str_new from wip_str_trans where str_new like @AND_OP_M and char_length(str_new)>=169 and char_length(str_new)<170 and str_new regexp '人';  -- match exact



-- select *  from wip_str_trans where char_length(str_new)>100;
update dcm_srch_str_term m inner join wip_str_trans w on m.type = 's' and w.origin<>w.str_new and m.srch_str = w.origin set m.srch_str = w.str_new;


--  select * from dcm_srch_str_term where type = 's' and srch_str regexp '&&' and srch_str not regexp '&&[0-9]';
--  select * from dcm_srch_str_term where type='s' ;
-- select * from dcm_srch_str_term where type ='s' and srch_str != str;

-- select * from dcm_srch_str_term where type = 'c' and str like '%(%)%';

-- 处理公司名字  company name
drop table if exists wip_str_trans;
create table wip_str_trans
as 
select distinct srch_str as origin, srch_str as str_raw, srch_str as str_new , srch_str as seg_new, srch_str as seg_ret from dcm_srch_str_term where type ='c' and srch_str <>'';  -- 764

ALTER TABLE wip_str_trans ADD  INDEX `ori_index` (`origin` );

-- select * from dcm_srch_str_term where type ='c';

set @delim := ' '; -- 用空格来分隔开 中英文 

-- update wip_str_trans set str_new  =   translate_alias(str_new,'w');
update wip_str_trans  set str_new =   translate_alias(str_new,'c')  ; -- 56
update wip_str_trans  set str_new =   translate_alias(str_new,'c')  ; -- double processing

call cleanStrExtraDelims();

update wip_str_trans  set seg_new = trim(get_char(str_new, @delim, 'c'));
update wip_str_trans  set str_new = concat_ws(@delim, seg_new,trim(replace(str_new,seg_new,''))); -- add empty space to match the end

-- select * from wip_str_trans  where str_new != str_raw;

-- select * from wip_str_trans  where seg_new != str_raw and seg_new !='';

call translateCompanyNameEn(); -- 1 


call translateCompanyName();
-- select * from wip_str_trans w where str_new<>str_raw;   
-- update wip_str_trans  set str_raw = str_new;
-- update wip_str_trans  set str_new = str_raw;

call removeCompanyFix();

-- select * from wip_str_trans w where origin regexp 'bayer' order by origin;  
 
-- select * from wip_str_trans w where origin regexp '[a-zA-Z]' order by origin;  
 
-- update wip_str_trans  set str_raw = str_new;

update wip_str_trans set str_new =  replace(str_new,@delim,'|');

update wip_str_trans set str_new = remove_duplicate_seg('|',str_new,0);

update wip_str_trans set str_new =  replace(str_new,'|','');

-- select * from wip_str_trans w where trim(str_new)<>trim(str_raw);   
-- update wip_str_trans set str_new = replace (str_new,' ','');

update dcm_srch_str_term m inner join wip_str_trans w on m.srch_str = w.origin and m.type = 'c' set m.srch_str = w.str_new;
             --  where w.str_new !=''; -- 756
--  select * from dcm_srch_str_term where type='c' and str <> srch_str

-- general final clean up 

update dcm_srch_str_term set srch_str = replace(srch_str,'(','') where srch_str like '%(%';
update dcm_srch_str_term set srch_str = replace(srch_str,')','') where srch_str like '%)%';
update dcm_srch_str_term set srch_str = replace(srch_str,' ','') where srch_str like '% %';

update dcm_srch_str_term set srch_str = remove_duplicate_seg(@OR_OP, srch_str,0) where srch_str like @OR_OP_M;
update dcm_srch_str_term set srch_str = remove_duplicate_seg(@AND_OP, srch_str,0) where srch_str like @AND_OP_M;
update dcm_srch_str_term set srch_str = move_andseg_to_end(srch_str);

update dcm_srch_str_term set srch_str = trim(srch_str);

-- 7383
 -- select count(*) from (
-- select w.srch_str, n.name_en, n.shrt_name from dcm_srch_str_term w, company_imp_name n where w.type='c' and  w.srch_str regexp n.name_en
-- ) a;
 


INSERT INTO dcm_srch_term  -- 4132
(`srch_str`,
`type`) 
select distinct d.srch_str, d.type
from dcm_srch_str_term d;

delete from dcm_srch_term where srch_str='' or type ='';

-- select srch_str,substring(srch_str,1,INSTR(srch_str, @OR_OP )-1) from dcm_srch_term where srch_str like @OR_OP_M;
update dcm_srch_term set srch_shrt_str = substring(srch_str,1,INSTR(srch_str, @OR_OP )-1) where srch_str like  @OR_OP_M;
update dcm_srch_term set srch_shrt_str = srch_str where srch_shrt_str =''; 
--  and srch_str not like  @AND_OP_M ;

update  dcm_srch_term set srch_shrt_str  = replace (srch_shrt_str, '[^.0-9]','') where srch_shrt_str like '%[%]%';
update  dcm_srch_term set srch_shrt_str  = replace (srch_shrt_str, '%','\%') where srch_shrt_str like '%\%%';

-- select * from dcm_srch_term where srch_shrt_str like '%\%%'
-- select * from dcm_srch_term where srch_shrt_str like '%[%]%'

-- select * from dcm_srch_term where srch_shrt_str ='';

-- 用第一个没有regrex的segment 做 search short string

-- select count(*) from dcm_srch_term where type='s';
-- select  distinct srch_str from dcm_srch_str_term where type='s';

-- select * from dcm_srch_x_data


INSERT INTO dcm_srch_x_data  -- 5628
(`data_id`,`srch_id`,`srch_str`,`type`)
select m.id as data_id, s.id as srch_id, s.srch_str,s.type from dcm_data_wip m, dcm_srch_str_term d, dcm_srch_term s where s.type = 'a' and s.srch_str = d.srch_str and d.str = m.an_raw
union 
select m.id as data_id, s.id as srch_id , s.srch_str,s.type from dcm_data_wip m, dcm_srch_str_term d, dcm_srch_term s where s.type = 'n' and s.srch_str = d.srch_str and d.str = m.name_raw
union 
select m.id as data_id, s.id as srch_id , s.srch_str,s.type from dcm_data_wip m, dcm_srch_str_term d, dcm_srch_term s where s.type = 'c' and s.srch_str = d.srch_str and d.str = m.company_raw
union 
select m.id as data_id, s.id as srch_id, s.srch_str,s.type from dcm_data_wip m, dcm_srch_str_term d, dcm_srch_term s where s.type = 's' and s.srch_str = d.srch_str and d.str = m.spec_raw
union 
select m.id as data_id, s.id as srch_id, s.srch_str,s.type from dcm_data_wip m, dcm_srch_str_term d, dcm_srch_term s where s.type = 'd' and s.srch_str = d.srch_str and d.str = m.df_raw
;

-- select * from dcm_srch_x_data

update dcm_data_wip m inner join dcm_srch_x_data s on m.id = s.data_id and s.type = 'n' set m.name_srch_id = s.srch_id, m.name_srch = s.srch_str;
update dcm_data_wip m inner join dcm_srch_x_data s on m.id = s.data_id and s.type = 'a' set m.an_srch_id = s.srch_id, m.an_srch = s.srch_str;
update dcm_data_wip m inner join dcm_srch_x_data s on m.id = s.data_id and s.type = 'd' set m.df_srch_id = s.srch_id, m.df_srch = s.srch_str;
update dcm_data_wip m inner join dcm_srch_x_data s on m.id = s.data_id and s.type = 's' set m.spec_srch_id = s.srch_id, m.spec_srch = s.srch_str;
update dcm_data_wip m inner join dcm_srch_x_data s on m.id = s.data_id and s.type = 'c' set m.company_srch_id = s.srch_id, m.company_srch = s.srch_str;

drop table if exists dcm_data_wip_bak;
create table dcm_data_wip_bak like dcm_data_wip;
insert into dcm_data_wip_bak select * from dcm_data_wip;

    

-- truncate table dcm_drug_str_sim_score; 
-- select count(*) from dcm_drug_str_sim_score where score is null;

drop table if exists dcm_res_wip;

CREATE TABLE `dcm_res_wip` (
  id_s int unsigned not null,
  id_m int unsigned not null,
  an_m varchar(100) not null,
  score smallint default -1,
  is_scoring smallint default 1,
  sub_score smallint default 0,
  rank smallint default null,
  `an_score` smallint default null,
   an_s_srch_id int unsigned,
   an_m_srch_id int unsigned, 
  `name_score` smallint default null,
   name_s_srch_id int unsigned,
   name_m_srch_id int unsigned, 
  `df_score` smallint default null,
   df_s_srch_id int unsigned,
   df_m_srch_id int unsigned, 
  `spec_score` smallint default null,
   spec_s_srch_id int unsigned,
   spec_m_srch_id int unsigned, 
   `company_score` smallint default null,
   company_s_srch_id int unsigned,
   company_m_srch_id int unsigned, 
   `src` varchar(15) NOT NULL DEFAULT '',
  `srch_t` char(2) NOT NULL DEFAULT '',  
  `srch_iter` smallint unsigned default 1,  
  `note` varchar(500) NOT NULL DEFAULT '',
   index (score),
   index (id_s),
   primary key (id_s,id_m)   
   ) 
    ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists dcm_res_wip_que;
create table dcm_res_wip_que like dcm_res_wip;

alter table dcm_res_wip add index (rank),
  add index (is_scoring),
  add index (id_m),
  add index (an_m),
  add index (name_score),
  add index (spec_score),
  add index (company_score),
  add index (df_score),
  add index (name_s_srch_id),
  add index (name_m_srch_id),
  add index (company_s_srch_id),
  add index (company_m_srch_id);

drop table if exists dcm_drug_str_sim_score;

CREATE TABLE `dcm_drug_str_sim_score` (
  `dcm_srch_id` int unsigned NOT NULL,
  `dcm_srch_str` varchar(500) default '',
  `drug_srch_id` int(11) unsigned NOT NULL,
  `drug_srch_str` varchar(500) default '',
  score smallint unsigned default null
--   case_id int(11) unsigned default NULL,
--  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
)
--  ENGINE= MyISAM DEFAULT CHARSET=utf8;
  ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `dcm_drug_str_sim_score`  --    80546 221s  143154 424
(`dcm_srch_id`, `dcm_srch_str`, `drug_srch_id`,`drug_srch_str`, score)
select distinct d.id as dcm_srch_id, d.srch_str as dcm_srch_str,
m.id as drug_srch_id ,
m.srch_str as drug_srch_str, 101
from 
dcm_srch_term d, srch_drug_term m
where  d.srch_shrt_str !='' and m.srch_str!='' and d.type= m.type and m.srch_str like concat('%',d.srch_shrt_str,'%');

update dcm_drug_str_sim_score set score = calc_similarity_w_or_and(0, dcm_srch_str, drug_srch_str)
where  (drug_srch_str like @AND_OP_M and dcm_srch_str not like @AND_OP_M  ) and drug_srch_str <> dcm_srch_str;

-- todo 氟康唑&&氯化钠		大扶康||fluconazoleandsodiumchlorideinjection||diflucan||&&氟康唑&&氯化钠注射液
-- select * from dcm_drug_str_sim_score where drug_srch_str like @AND_OP_M and dcm_srch_str like @AND_OP_M and drug_srch_str <> dcm_srch_str;
-- select * from dcm_drug_str_sim_score where drug_srch_str like @AND_OP_M and drug_srch_str <> dcm_srch_str;
-- select * from dcm_drug_str_sim_score where drug_srch_str like @AND_OP_M and drug_srch_str = dcm_srch_str;
-- select calc_similarity_w_or_and(0,'丁苯酞','丁苯酞&&氯化钠注射液');

alter table `dcm_drug_str_sim_score` add 
  key (score),
  add PRIMARY KEY (dcm_srch_id,drug_srch_id);
-- select * from srch_drug_term m where type = 'c'  and str regexp 'aventis';
-- select * from dcm_srch_term m where type = 's' ;
-- select * from dcm_srch_str_term where type ='n' order by char_length(str);
--  select * from dcm_data_wip where name_srch ='n||l丙氨酰l谷氨酰胺'
-- select * from dcm_data_wip where name_raw = '腹膜透析液 (乳酸盐-G1.5%)' limit 1000;
-- select * from dcm_drug_str_sim_score where type ='n' and score > 0 order by score  ;
-- 
-- select * from v_dcm_drug_str_sim_score where dcm_type ='c' and score =101 order by score limit 1000; 
-- select * from v_dcm_drug_str_sim_score where dcm_type ='d' order by score limit 1000; 
-- select * from v_dcm_drug_str_sim_score where dcm_type ='s' order by score limit 1000; 
-- select * from v_dcm_drug_str_sim_score where dcm_type ='n' order by score limit 1000; 

 select distinct dcm_srch_id,dcm_srch_str, dcm_type, count(*) from v_dcm_drug_str_sim_score
 where dcm_srch_id in 
 (select  dcm_srch_id from dcm_drug_str_sim_score  group by dcm_srch_id having count(*) > 300
 ) group by dcm_srch_id, dcm_srch_str, dcm_type order by count(*) limit 1000;

-- select * from mv_drug_srch where company_srch regexp  '远大' and name regexp '伐'

select count(*) from srch_drug_term;
SET FOREIGN_KEY_CHECKS = 1;
-- select * from dcm_data_wip